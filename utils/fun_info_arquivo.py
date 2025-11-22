import os

def ler_dados_csv(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []

    dados_limpos = []
    
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
        
        # enumerate(linhas) nos dá (0, 'Data...'), (1, 'Data...')
        for i, linha in enumerate(linhas):
            # Ignora cabeçalho ou linhas vazias
            if i == 0 or not linha.strip():
                continue

            colunas = linha.strip().split(',')
            
            if len(colunas) >= 3:
                # O TRUQUE: Adicionamos o índice 'i' como um 4º elemento escondido
                # Lista fica: [Data, Hora, Valor, ID_Original]
                colunas.append(i) 
                dados_limpos.append(colunas)
                
    return dados_limpos