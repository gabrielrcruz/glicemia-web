# utils/fun_dados_estatisticos.py
from datetime import datetime

def relatorio_completo_master(lista_dados):
    valores = []
    horas_dict = {h: [] for h in range(24)}
    dias_semana_dict = {i: [] for i in range(7)} 
    nomes_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    
    # Contadores para os períodos do dia
    periodos_count = {"Manhã": 0, "Tarde": 0, "Noite": 0}

    # O loop começa do índice 1 para pular o cabeçalho
    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        try:
            val = float(linha[2])
            valores.append(val)
            
            # --- Análise Horária e Períodos ---
            hora_full = linha[1]
            h_int = int(hora_full.split(':')[0])
            
            if 0 <= h_int <= 23:
                horas_dict[h_int].append(val)

                # Lógica dos Períodos
                # Manhã: 06:00 às 11:59
                # Tarde: 12:00 às 17:59
                # Noite: 18:00 às 05:59
                if 6 <= h_int < 12:
                    periodos_count["Manhã"] += 1
                elif 12 <= h_int < 18:
                    periodos_count["Tarde"] += 1
                else:
                    periodos_count["Noite"] += 1

            # --- Análise Dia da Semana ---
            data_str = linha[0]
            dt_obj = datetime.strptime(data_str, '%Y-%m-%d')
            dias_semana_dict[dt_obj.weekday()].append(val)

        except ValueError:
            continue

    if not valores: return None

    # --- Estatísticas Básicas ---
    media = sum(valores) / len(valores)
    
    # --- Processar Padrão Horário (Melhor/Pior glicemia) ---
    piores_horas = []
    melhores_horas = []
    
    for h in range(24):
        lista_h = horas_dict[h]
        if lista_h:
            media_h = sum(lista_h) / len(lista_h)
            if media_h > media: 
                piores_horas.append({'hora': h, 'media': round(media_h)})
            else:
                melhores_horas.append({'hora': h, 'media': round(media_h)})
    
    piores_horas.sort(key=lambda x: x['media'], reverse=True)
    melhores_horas.sort(key=lambda x: x['media'], reverse=False)
    
    # --- Processar Padrão Semanal e Frequência ---
    analise_dias = []
    lista_qtd_dias = [] # Lista auxiliar para achar dia com mais/menos medições

    for i in range(7):
        lista_d = dias_semana_dict[i]
        qtd = len(lista_d)
        
        # Salva para o ranking de QUANTIDADE
        lista_qtd_dias.append({'dia_nome': nomes_dias[i], 'qtd': qtd})

        if lista_d:
            media_d = sum(lista_d) / len(lista_d)
            analise_dias.append({
                'dia_nome': nomes_dias[i],
                'media': round(media_d),
                'qtd': qtd
            })
    
    # Ordena tabela principal pela MÉDIA GLICÊMICA (Pior -> Melhor)
    analise_dias.sort(key=lambda x: x['media'], reverse=True)

    # --- NOVAS FUNCIONALIDADES: Rankings de Quantidade ---

    # 1. Dias com Mais e Menos Medições
    lista_qtd_dias.sort(key=lambda x: x['qtd']) # Crescente (0..10..100)
    dia_menos_freq = lista_qtd_dias[0]  # Primeiro da lista (Menor)
    dia_mais_freq = lista_qtd_dias[-1]  # Último da lista (Maior)

    # 2. Períodos com Mais e Menos Medições
    # Converte dicionário em lista de tuplas e ordena
    lista_periodos = sorted(periodos_count.items(), key=lambda item: item[1])
    # Ex: [('Noite', 5), ('Tarde', 10), ('Manhã', 20)]
    
    periodo_menos_freq = {'nome': lista_periodos[0][0], 'qtd': lista_periodos[0][1]}
    periodo_mais_freq = {'nome': lista_periodos[-1][0], 'qtd': lista_periodos[-1][1]}

    return {
        "media_global": round(media, 2),
        "total_medicoes": len(valores),
        "pior_hora": piores_horas[0] if piores_horas else None, 
        "melhor_hora": melhores_horas[0] if melhores_horas else None,
        "ranking_dias": analise_dias,
        # Novos dados de frequência
        "dia_menos": dia_menos_freq,
        "dia_mais": dia_mais_freq,
        "periodo_menos": periodo_menos_freq,
        "periodo_mais": periodo_mais_freq
    }