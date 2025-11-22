# utils/fun_dados_estatisticos.py
from datetime import datetime

def relatorio_completo_master(lista_dados):
    valores = []
    horas_dict = {h: [] for h in range(24)}
    dias_semana_dict = {i: [] for i in range(7)} 
    nomes_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    
    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        try:
            val = float(linha[2])
            valores.append(val)
            
            # Análise Horária
            hora_full = linha[1]
            h_int = int(hora_full.split(':')[0])
            if 0 <= h_int <= 23:
                horas_dict[h_int].append(val)

            # Análise Dia da Semana
            data_str = linha[0]
            dt_obj = datetime.strptime(data_str, '%Y-%m-%d')
            dias_semana_dict[dt_obj.weekday()].append(val)

        except ValueError:
            continue

    if not valores: return None

    # --- Estatísticas Básicas ---
    media = sum(valores) / len(valores)
    
    # --- Processar Padrão Horário ---
    piores_horas = []
    melhores_horas = []
    
    for h in range(24):
        lista_h = horas_dict[h]
        if lista_h:
            media_h = sum(lista_h) / len(lista_h)
            
            # Critério: Se a média da hora for maior que a média global, entra nos "piores"
            if media_h > media: 
                piores_horas.append({'hora': h, 'media': round(media_h)})
            else:
                melhores_horas.append({'hora': h, 'media': round(media_h)})
    
    # ORDENAÇÃO (AQUI ESTAVA O ERRO)
    # Piores: ordena do Maior para o Menor (reverse=True) -> Queremos o pico mais alto
    piores_horas.sort(key=lambda x: x['media'], reverse=True)
    
    # Melhores: ordena do Menor para o Maior (reverse=False) -> Queremos a média mais baixa
    melhores_horas.sort(key=lambda x: x['media'], reverse=False)
    
    # --- Processar Padrão Semanal ---
    analise_dias = []
    for i in range(7):
        lista_d = dias_semana_dict[i]
        if lista_d:
            media_d = sum(lista_d) / len(lista_d)
            analise_dias.append({
                'dia_nome': nomes_dias[i],
                'media': round(media_d),
                'qtd': len(lista_d)
            })
    
    # Ordena dias do pior (maior média) para o melhor
    analise_dias.sort(key=lambda x: x['media'], reverse=True)

    return {
        "media_global": round(media, 2),
        "total_medicoes": len(valores),
        "pior_hora": piores_horas[0] if piores_horas else None, 
        "melhor_hora": melhores_horas[0] if melhores_horas else None,
        "ranking_dias": analise_dias 
    }