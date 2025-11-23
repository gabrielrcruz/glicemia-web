from flask import Flask, flash,render_template, request, redirect, url_for, Response
import os

# --- IMPORTAÇÕES ORGANIZADAS ---
from utils.gerenciador_arquivo import salvar_novas_medicoes, excluir_registro_por_id, atualizar_registro_por_id
from utils.fun_info_arquivo import ler_dados_csv
from utils.fun_dados_estatisticos import relatorio_completo_master
from utils.analises import calcular_tempo_no_alvo, calcular_hba1c_estimada, calcular_variabilidade
from utils.filtros import filtrar_por_faixa, agrupar_medias_diarias
from utils.busca import buscar_dados
from utils.frequencia import calcular_frequencia_diaria
from utils.exportacao import gerar_csv_para_download 
from utils.processador_upload import processar_arquivo_upload

app = Flask(__name__)

app.secret_key = "sua_chave_secreta_aqui" # Necessário para usar flash messages (feedback)
# Configuração: Caminho do arquivo
ARQUIVO_CSV = 'dados_glicemia.csv'

# --- ROTA INICIAL (DASHBOARD) ---
@app.route('/')
def index():
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    if not dados_limpos:
        return "Erro: Arquivo de dados não encontrado ou vazio."

    stats_master = relatorio_completo_master(dados_limpos)
    tir = calcular_tempo_no_alvo(dados_limpos)
    hba1c = calcular_hba1c_estimada(dados_limpos)
    variabilidade = calcular_variabilidade(dados_limpos)
    ultimas_medicoes = dados_limpos[::-1][:10]

    return render_template('index.html', 
                           estatisticas=stats_master,
                           tempo_alvo=tir,
                           glicada=hba1c,
                           var=variabilidade,
                           dados=ultimas_medicoes)

# --- ROTA PARA LISTAS FILTRADAS ---
@app.route('/filtros/<tipo>', methods=['GET', 'POST'])
def pagina_filtros(tipo):
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    resultado = filtrar_por_faixa(dados_limpos, tipo)
    
    # Verifica se o botão de download foi apertado
    acao = request.form.get('acao')
    
    if acao == 'baixar':
        csv_conteudo = gerar_csv_para_download(resultado) 
        return Response(
            csv_conteudo,
            mimetype="text/csv",
            headers={"Content-disposition": f"attachment; filename=relatorio_{tipo}.csv"}
        )
    
    # IMPORTANTE: Passe 'tipo_filtro=tipo' para o template saber quem ele é
    return render_template('tabela.html', 
                           lista=resultado, 
                           titulo=f"Filtro: {tipo}", 
                           tipo_filtro=tipo)

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

# --- ROTA DE BUSCA COM DOWNLOAD ---
@app.route('/busca', methods=['GET', 'POST'])
def pagina_busca():
    resultados = []
    
    if request.method == 'POST':
        dados_limpos = ler_dados_csv(ARQUIVO_CSV)
        dt_ini = request.form.get('data_inicio')
        dt_fim = request.form.get('data_fim')
        v_min = request.form.get('valor_min')
        v_max = request.form.get('valor_max')
        
        resultados = buscar_dados(dados_limpos, dt_ini, dt_fim, v_min, v_max)
        
        acao = request.form.get('acao')
        
        if acao == 'baixar':
            csv_conteudo = gerar_csv_para_download(resultados) 
            return Response(
                csv_conteudo,
                mimetype="text/csv",
                headers={"Content-disposition": "attachment; filename=dados_filtrados.csv"}
            )
            
    return render_template('busca.html', resultados=resultados)

# --- ROTA DE UPLOAD ---
@app.route('/adicionar', methods=['POST'])
def adicionar_dados():
    novos_dados_texto = request.form.get('novos_dados')
    if novos_dados_texto:
        linhas = novos_dados_texto.split('\n')
        sucesso, msg = salvar_novas_medicoes(ARQUIVO_CSV, linhas)
        if sucesso:
            print(f"Sucesso: {msg} registros adicionados.")
        else:
            print(f"Erro: {msg}")
    return redirect(url_for('index'))

# --- ROTA RELATÓRIO MASTER (ATUALIZADA) ---
@app.route('/relatorio-master')
def pagina_relatorio_master():
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    # A função agora retorna os dados de frequência também
    insights = relatorio_completo_master(dados_limpos)
    return render_template('relatorio_master.html', info=insights)

# --- ROTA DELETAR ---
@app.route('/deletar/<int:id_linha>')
def deletar(id_linha):
    sucesso, msg = excluir_registro_por_id(ARQUIVO_CSV, id_linha)
    return redirect(request.referrer or url_for('index'))

# --- ROTA EDITAR ---
@app.route('/editar/<int:id_linha>', methods=['GET', 'POST'])
def editar(id_linha):
    if request.method == 'POST':
        nova_data = request.form.get('data')
        nova_hora = request.form.get('hora')
        novo_valor = request.form.get('valor')
        atualizar_registro_por_id(ARQUIVO_CSV, id_linha, nova_data, nova_hora, novo_valor)
        return redirect(url_for('index'))
    else:
        try:
            with open(ARQUIVO_CSV, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                linha_atual = linhas[id_linha].strip().split(',')
            return render_template('editar.html', id=id_linha, dado=linha_atual)
        except:
            return "Erro ao carregar linha para edição."

# --- ROTA LISTA COMPLETA ---
@app.route('/dados')
def ver_lista_completa():
    dados_limpos = ler_dados_csv(ARQUIVO_CSV)
    dados_invertidos = dados_limpos[::-1]
    return render_template('tabela.html', lista=dados_invertidos, titulo="Histórico Completo de Medições")


# --- NOVA ROTA: UPLOAD DE ARQUIVO ---
@app.route('/upload', methods=['POST'])
def upload_arquivo():
    # Verifica se o arquivo está na requisição
    if 'arquivo_csv' not in request.files:
        flash('Nenhum arquivo selecionado.')
        return redirect(url_for('index'))
    
    arquivo = request.files['arquivo_csv']
    
    # Verifica se o nome está vazio
    if arquivo.filename == '':
        flash('Nenhum arquivo selecionado.')
        return redirect(url_for('index'))

    # Verifica a extensão (Somente CSV)
    if arquivo and arquivo.filename.endswith('.csv'):
        try:
            # Processa o arquivo usando a nova função
            dados_formatados, qtd = processar_arquivo_upload(arquivo)
            
            if qtd > 0:
                # Salva no arquivo principal usando a função que você já tem
                salvar_novas_medicoes(ARQUIVO_CSV, dados_formatados)
                flash(f'Sucesso! {qtd} novas medições foram importadas do arquivo {arquivo.filename}.')
            else:
                flash('O arquivo foi lido, mas nenhuma medição válida foi encontrada ou o formato está incorreto.')
                
        except Exception as e:
            flash(f'Erro ao processar arquivo: {str(e)}')
    else:
        flash('Formato inválido. Por favor, envie apenas arquivos .csv')

    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)