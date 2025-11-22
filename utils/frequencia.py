# utils/frequencia.py

def calcular_frequencia_diaria(lista_dados):
    """
    Conta quantos testes foram feitos por dia.
    """
    contagem = {}
    total_geral = 0
    
    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        try:
            float(linha[2]) # Só conta se o valor for válido
            data = linha[0]
            contagem[data] = contagem.get(data, 0) + 1
            total_geral += 1
        except ValueError:
            continue

    if total_geral == 0: return []

    resultado = []
    for data in sorted(contagem.keys()):
        qtd = contagem[data]
        pct = (qtd / total_geral) * 100
        resultado.append({
            "data": data,
            "qtd": qtd,
            "porcentagem": round(pct, 1)
        })
        
    return resultado