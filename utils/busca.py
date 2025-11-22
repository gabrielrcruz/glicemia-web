# utils/busca.py

def buscar_dados(lista_dados, data_inicio=None, data_fim=None, valor_min=None, valor_max=None):
    """
    Filtra a lista principal baseada nos argumentos opcionais.
    Retorna uma NOVA lista contendo apenas os resultados.
    """
    resultados = []
    
    # Converte valores string para numérico se existirem
    v_min = int(valor_min) if valor_min else None
    v_max = int(valor_max) if valor_max else None
    
    for linha in lista_dados[1:]: # Pula cabeçalho
        if len(linha) < 3: continue
        
        try:
            data = linha[0]
            # Assumindo que o valor é float/int
            valor = float(linha[2])
            
            # Aplica Filtros
            if data_inicio and data < data_inicio: continue
            if data_fim and data > data_fim: continue
            if v_min is not None and valor < v_min: continue
            if v_max is not None and valor > v_max: continue
            
            # Se passou, adiciona
            resultados.append(linha)
            
        except ValueError:
            continue
            
    return resultados