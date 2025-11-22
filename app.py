from flask import Flask, render_template, request, redirect, url_for
import os

# --- Importando suas funções da pasta utils ---
from utils.gerenciador_arquivo import salvar_novas_medicoes, excluir_registro_por_id, atualizar_registro_por_id
from utils.fun_info_arquivo import ler_dados_csv
from utils.fun_dados_estatisticos import relatorio_completo_master
from utils.analises import calcular_tempo_no_alvo, calcular_hba1c_estimada, calcular_variabilidade
from utils.filtros import filtrar_por_faixa, agrupar_medias_diarias
from utils.busca import buscar_dados
from utils.frequencia import calcular_frequencia_diaria
from utils.gerenciador_arquivo import salvar_novas_medicoes
from flask import Response 
from utils.exportacao import gerar_csv_para_download 

app = Flask(__name__)

# Configuração: Caminho do arquivo
ARQUIVO_CSV = 'dados_glicemia.csv'

# --- ROTA INICIAL (DASHBOARD) ---
@app.route('/')
def index():
    # 1. CARREGAMOS OS DADOS AQUI
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    
    # Se o arquivo estiver vazio ou não existir
    if not dados_limpos:
        return "Erro: Arquivo de dados não encontrado ou vazio."

    # 2. Chamamos as funções passando os dados carregados
    stats_master = relatorio_completo_master(dados_limpos)
    tir = calcular_tempo_no_alvo(dados_limpos)
    hba1c = calcular_hba1c_estimada(dados_limpos)
    variabilidade = calcular_variabilidade(dados_limpos)
    ultimas_medicoes = dados_limpos[::-1][:10]
    # 3. Enviamos tudo para o HTML
    return render_template('index.html', 
                           estatisticas=stats_master,
                           tempo_alvo=tir,
                           glicada=hba1c,
                           var=variabilidade,
                           dados=ultimas_medicoes)

# --- ROTA PARA LISTAS FILTRADAS (HIPO/HIPER/ALVO) ---
@app.route('/filtros/<tipo>')
def pagina_filtros(tipo):
    # Carrega dados novamente para garantir atualização
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    
    # Usa a função de filtro
    resultado = filtrar_por_faixa(dados_limpos, tipo)
    
    return render_template('tabela.html', lista=resultado, titulo=f"Filtro: {tipo}")

# --- ROTA PARA MÉDIA DIÁRIA ---
@app.route('/media-diaria')
def pagina_media_diaria():
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    resultado = agrupar_medias_diarias(dados_limpos)
    return render_template('media_diaria.html', dados=resultado)

# --- ROTA PARA FREQUÊNCIA ---
@app.route('/frequencia')
def pagina_frequencia():
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    freq = calcular_frequencia_diaria(dados_limpos)
    return render_template('tabela_frequencia.html', lista=freq)

# --- ROTA DE BUSCA ---
# --- ROTA DE BUSCA COM DOWNLOAD ---
# No app.py

@app.route('/busca', methods=['GET', 'POST'])
def pagina_busca():
    resultados = [] # Começa vazio
    
    if request.method == 'POST':
        # 1. Carrega TUDO
        dados_limpos = ler_dados_csv(ARQUIVO_CSV)
        
        # 2. Pega os filtros do HTML
        dt_ini = request.form.get('data_inicio')
        dt_fim = request.form.get('data_fim')
        v_min = request.form.get('valor_min')
        v_max = request.form.get('valor_max')
        
        # 3. APLICA O FILTRO (Crucial: isso tem que acontecer antes do download)
        resultados = buscar_dados(dados_limpos, dt_ini, dt_fim, v_min, v_max)
        
        # 4. Verifica qual botão foi apertado
        acao = request.form.get('acao')
        
        if acao == 'baixar':
            # O ERRO ESTAVA AQUI:
            # Você deve passar 'resultados' (que foi filtrado acima), 
            # e NÃO 'dados_limpos' (que é o arquivo inteiro).
            csv_conteudo = gerar_csv_para_download(resultados) 
            
            return Response(
                csv_conteudo,
                mimetype="text/csv",
                headers={"Content-disposition": "attachment; filename=dados_filtrados.csv"}
            )
            
    return render_template('busca.html', resultados=resultados)

# --- ROTA DE UPLOAD (ADICIONAR DADOS) ---
@app.route('/adicionar', methods=['POST'])
def adicionar_dados():
    # Pega o texto da área de texto do HTML
    novos_dados_texto = request.form.get('novos_dados')
    
    if novos_dados_texto:
        # Quebra o texto em uma lista de linhas
        linhas = novos_dados_texto.split('\n')
        
        sucesso, msg = salvar_novas_medicoes(ARQUIVO_CSV, linhas)
        if sucesso:
            print(f"Sucesso: {msg} registros adicionados.")
        else:
            print(f"Erro: {msg}")
            
    return redirect(url_for('index'))

@app.route('/relatorio-master')
def pagina_relatorio_master():
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    insights = relatorio_completo_master(dados_limpos)
    return render_template('relatorio_master.html', info=insights)

# --- ROTA PARA DELETAR ---
@app.route('/deletar/<int:id_linha>')
def deletar(id_linha):
    sucesso, msg = excluir_registro_por_id(ARQUIVO_CSV, id_linha)
    if sucesso:
        print(f"Linha {id_linha} excluída.")
    else:
        print(f"Erro: {msg}")
    # Volta para a página anterior ou para a home
    return redirect(request.referrer or url_for('index'))

# --- ROTA PARA ABRIR A TELA DE EDIÇÃO ---
@app.route('/editar/<int:id_linha>', methods=['GET', 'POST'])
def editar(id_linha):
    # Se for salvar a edição (POST)
    if request.method == 'POST':
        nova_data = request.form.get('data')
        nova_hora = request.form.get('hora')
        novo_valor = request.form.get('valor')
        
        sucesso, msg = atualizar_registro_por_id(ARQUIVO_CSV, id_linha, nova_data, nova_hora, novo_valor)
        return redirect(url_for('index')) # Volta pra home após salvar

    # Se for apenas abrir o formulário (GET)
    else:
        # Precisamos achar os dados atuais dessa linha para preencher o formulário
        # Vamos ler o arquivo bruto para pegar exatamente aquela linha
        try:
            with open(ARQUIVO_CSV, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                linha_atual = linhas[id_linha].strip().split(',')
                # linha_atual será algo como ['2025-10-10', '12:00', '98']
                
            return render_template('editar.html', id=id_linha, dado=linha_atual)
        except:
            return "Erro ao carregar linha para edição."
        
        # --- ROTA PARA LISTA COMPLETA (HISTÓRICO) ---
@app.route('/dados')
def ver_lista_completa():
    # 1. Carrega os dados
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    
    # 2. Inverte a lista para mostrar os mais recentes no topo (opcional, mas recomendado)
    # [::-1] faz a inversão da lista
    dados_invertidos = dados_limpos[::-1]
    
    # 3. Usa o mesmo template 'tabela.html' que usamos nos filtros
    return render_template('tabela.html', 
                           lista=dados_invertidos, 
                           titulo="Histórico Completo de Medições")

import os

if __name__ == "__main__":
    # Pega a porta do ambiente ou usa 8080 como padrão
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)