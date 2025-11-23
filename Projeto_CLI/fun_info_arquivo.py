def inf_arquivo(arquivo_csv):

    arquivo = open(arquivo_csv, "r")

    # 1. Lê todas as linhas
    linhas = arquivo.readlines()

    # 2. Cria uma lista vazia para guardar os dados limpos
    dados_limpos = []

    # 3. Passa por cada linha para limpar e separar
    for linha in linhas:
        # .strip() remove o \n do final
        # .split(',') quebra o texto onde tem vírgula
        colunas = linha.strip().split(',')
        
        dados_limpos.append(colunas)

    arquivo.close()

    # Agora você tem uma lista estruturada
    
    return dados_limpos


