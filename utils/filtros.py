# utils/filtros.py

def filtrar_por_faixa(lista_dados, tipo):
    """
    Retorna uma lista filtrada baseada no tipo:
    'hipo' (<70), 'hiper' (>180), 'alvo' (70-150)
    """
    resultado = []
    
    for linha in lista_dados[1:]: # Pula cabeçalho
        if len(linha) < 3: continue
        
        try:
            val = float(linha[2])
            
            match = False
            if tipo == 'hipo' and val < 70:
                match = True
            elif tipo == 'hiper' and val > 180:
                match = True
            elif tipo == 'alvo' and 70 <= val <= 150: # Notei que seu código original usava 150 aqui
                match = True
                
            if match:
                resultado.append(linha)
                
        except ValueError:
            continue
            
    return resultado

def obter_dados_ordenados(lista_dados, decrescente=True):
    """
    Retorna a lista de dados ordenada pelo valor da glicemia.
    """
    # 1. Limpa dados inválidos
    dados_validos = []
    for linha in lista_dados[1:]:
        if len(linha) >= 3:
            try:
                float(linha[2]) # Testa se é numero
                dados_validos.append(linha)
            except ValueError:
                continue
                
    # 2. Ordena
    # key=lambda x: float(x[2]) diz para ordenar baseado na coluna Valor convertida para numero
    dados_validos.sort(key=lambda x: float(x[2]), reverse=decrescente)
    
    return dados_validos

def agrupar_medias_diarias(lista_dados):
    """
    Retorna uma lista de dicionários com: Data, Média e Quantidade.
    """
    agrupamento = {} # Dicionário temporário: {'2025-10-08': [100, 120]}

    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        try:
            data = linha[0]
            val = float(linha[2])
            
            if data not in agrupamento:
                agrupamento[data] = []
            agrupamento[data].append(val)
        except ValueError:
            continue

    # Transforma o dicionário em uma lista organizada para o HTML
    lista_final = []
    for data in sorted(agrupamento.keys()):
        vals = agrupamento[data]
        media = sum(vals) / len(vals)
        lista_final.append({
            "data": data,
            "media": round(media, 2),
            "qtd": len(vals)
        })
        
    return lista_final