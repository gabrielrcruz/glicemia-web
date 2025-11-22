import io
import csv

def gerar_csv_para_download(dados):
    """
    Recebe uma lista de dados e retorna uma string formatada como CSV
    pronta para ser enviada ao navegador.
    """
    # Cria um arquivo na memória (não no disco)
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escreve o cabeçalho
    writer.writerow(['Data', 'Hora', 'Valor'])
    
    # Escreve os dados
    writer.writerows(dados)
    
    # Retorna o conteúdo texto do CSV
    return output.getvalue()