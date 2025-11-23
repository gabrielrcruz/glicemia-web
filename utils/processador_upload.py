# utils/processador_upload.py
from datetime import datetime
import io

def processar_arquivo_upload(file_storage):
    """
    Processa CSV específico onde:
    - Coluna 4: Data e Hora juntas (dd/mm/yyyy HH:MM)
    - Coluna 7: Valor da Glicemia
    """
    dados_processados = []
    
    # 1. Decodificação Robusta (UTF-8 -> Latin-1 -> CP1252)
    conteudo_bytes = file_storage.stream.read()
    texto = ""
    try:
        texto = conteudo_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            texto = conteudo_bytes.decode("latin-1")
        except:
            texto = conteudo_bytes.decode("cp1252", errors='ignore')

    stream = io.StringIO(texto, newline=None)
    
    print("--- INICIANDO PROCESSAMENTO DE NOVO FORMATO ---")

    for linha in stream:
        linha = linha.strip()
        # Ignora linhas vazias ou linhas de metadados que começam com ;;
        if not linha or linha.startswith(";;"): 
            continue

        partes = linha.split(';')

        # O arquivo tem muitas colunas, precisamos garantir que tenha pelo menos até o índice 7 (Valor)
        if len(partes) < 8:
            continue

        # Extração baseada nas colunas que você enviou:
        # Coluna 4 (índice 4): DataTime -> "21/11/2025 06:47"
        # Coluna 7 (índice 7): Valor -> "354"
        
        coluna_datatime = partes[4].strip()
        coluna_valor = partes[7].strip()

        # Pula o cabeçalho textual (se a linha for o cabeçalho "DataTime")
        if "DataTime" in coluna_datatime or not coluna_valor.isdigit():
            continue

        try:
            # 1. Separa Data e Hora da string "21/11/2025 06:47"
            # O formato é dia/mês/ano hora:minuto
            dt_obj = datetime.strptime(coluna_datatime, "%d/%m/%Y %H:%M")
            
            # Converte para os formatos padrão do sistema
            data_formatada = dt_obj.strftime("%Y-%m-%d") # 2025-11-21
            hora_formatada = dt_obj.strftime("%H:%M:00") # 06:47:00

            # 2. Formata linha final
            linha_csv = f"{data_formatada},{hora_formatada},{coluna_valor}"
            dados_processados.append(linha_csv)

        except ValueError:
            # Se der erro na data (formato diferente), pula a linha
            continue

    print(f"--- FIM: {len(dados_processados)} medições importadas ---")
    return dados_processados, len(dados_processados)