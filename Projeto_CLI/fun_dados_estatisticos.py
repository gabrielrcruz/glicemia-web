from datetime import datetime

def calcular_mediana(valores):
    """Função auxiliar para calcular mediana de uma lista ordenada"""
    n = len(valores)
    if n == 0: return 0
    
    valores_sorted = sorted(valores)
    
    # Se for par, média dos dois do meio
    if n % 2 == 0:
        meio1 = valores_sorted[n//2]
        meio2 = valores_sorted[n//2 - 1]
        return (meio1 + meio2) / 2
    else:
        # Se for ímpar, pega o do meio exato
        return valores_sorted[n//2]

def gerar_relatorio_completo(lista_dados):
    print("\n=== RELATÓRIO ESTATÍSTICO MASTER ===")
    print("Calculando métricas, padrão horário e dias da semana...")
    
    # --- 1. Setup de Variáveis ---
    valores = []
    horas_dict = {h: [] for h in range(24)}
    
    # 0=Segunda, 1=Terça ... 6=Domingo
    dias_semana_dict = {i: [] for i in range(7)} 
    nomes_dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    
    linhas_totais_lidas = len(lista_dados) - 1
    linhas_validas = 0

    # --- 2. Loop Principal (Extração) ---
    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        
        try:
            # Extrai Valor
            val = int(float(linha[2]))
            valores.append(val)
            linhas_validas += 1

            # Análise Horária
            hora_str = linha[1]
            h_int = int(hora_str.split(':')[0])
            if 0 <= h_int <= 23:
                horas_dict[h_int].append(val)

            # Análise Dia da Semana
            data_str = linha[0] # "2025-10-08"
            # Converte string para data real para saber o dia da semana
            dt_obj = datetime.strptime(data_str, '%Y-%m-%d')
            dia_idx = dt_obj.weekday() # Retorna 0 a 6
            dias_semana_dict[dia_idx].append(val)

        except ValueError:
            continue

    if not valores:
        print("Erro: Nenhum dado válido encontrado.")
        return

    # Ordenar para cálculos de quartis
    valores.sort()
    n = len(valores)

    # --- 3. Cálculos Estatísticos Básicos ---
    minimo = valores[0]
    maximo = valores[-1]
    media = sum(valores) / n
    porcentagem_validade = (linhas_validas / linhas_totais_lidas) * 100 if linhas_totais_lidas > 0 else 0

    # Desvio Padrão
    soma_diff_quad = sum((x - media) ** 2 for x in valores)
    if n > 1:
        desvio_padrao = (soma_diff_quad / (n - 1)) ** 0.5
    else:
        desvio_padrao = 0

    # Quartis e Mediana
    mediana = calcular_mediana(valores)
    metade_inferior = valores[:n//2]
    q1 = calcular_mediana(metade_inferior)
    if n % 2 == 0: metade_superior = valores[n//2:]
    else: metade_superior = valores[n//2 + 1:]
    q3 = calcular_mediana(metade_superior)

    # --- 4. Processamento: Padrão Horário ---
    pior_hora = -1
    pior_media_hora = -1
    melhor_hora = -1
    melhor_media_hora = 9999
    resumo_horas = {} 

    for h in range(24):
        lista_h = horas_dict[h]
        if lista_h:
            media_h = sum(lista_h) / len(lista_h)
            resumo_horas[h] = (media_h, len(lista_h), min(lista_h), max(lista_h))
            
            if media_h > pior_media_hora:
                pior_media_hora = media_h
                pior_hora = h
            if media_h < melhor_media_hora:
                melhor_media_hora = media_h
                melhor_hora = h
        else:
            resumo_horas[h] = None

    # --- 5. Processamento: Dias da Semana ---
    pior_dia_nome = ""
    pior_media_dia = -1
    
    resumo_dias = {} # Para salvar no CSV depois

    for i in range(7):
        lista_d = dias_semana_dict[i]
        if lista_d:
            media_d = sum(lista_d) / len(lista_d)
            resumo_dias[i] = (media_d, len(lista_d))
            
            # Verifica se esse é o dia com maior média glicêmica
            if media_d > pior_media_dia:
                pior_media_dia = media_d
                pior_dia_nome = nomes_dias[i]
        else:
            resumo_dias[i] = None

    # --- 6. Impressão no Terminal ---
    print("-" * 50)
    print(f"Total de Medições: {n}")
    print(f"Média Global: {media:.2f} mg/dL")
    print(f"Mediana: {mediana:.2f}")
    print(f"Desvio Padrão: {desvio_padrao:.2f}")
    print("-" * 50)
    
    # INSIGHTS DE HORÁRIO
    if pior_hora != -1 and melhor_hora != -1:
        print("ANÁLISE DE TENDÊNCIA HORÁRIA:")
        print(f"> Sobe às {pior_hora:02d}:00 (Média: {pior_media_hora:.0f})")
        print(f"> Cai às {melhor_hora:02d}:00 (Média: {melhor_media_hora:.0f})")
    
    # INSIGHTS DE DIA DA SEMANA
    if pior_dia_nome:
        print("\nANÁLISE SEMANAL:")
        print(f"> Sua glicemia tende a ser MAIS ALTA nas {pior_dia_nome}s.")
        print(f"> Média nesse dia: {pior_media_dia:.0f} mg/dL")
    else:
        print("Dados insuficientes para análise semanal.")

    print("-" * 50)

    # --- 7. Salvar Arquivo ---
    salvar = input("\nDeseja salvar este relatório detalhado em CSV? (s/n): ")

    if salvar.lower() in ['s', 'sim']:
        nome_arquivo = input("Nome do arquivo CSV: ")
        if not nome_arquivo.endswith('.csv'): nome_arquivo += '.csv'

        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                # BLOCO 1: Estatísticas Gerais
                f.write("=== ESTATISTICAS GERAIS ===\n")
                f.write("Metrica,Valor\n")
                f.write(f"Total de Medicoes,{n}\n")
                f.write(f"Minimo,{minimo}\n")
                f.write(f"Maximo,{maximo}\n")
                f.write(f"Media,{media:.2f}\n")
                f.write(f"Desvio Padrao,{desvio_padrao:.2f}\n")
                f.write(f"Mediana (Q2),{mediana:.2f}\n")
                f.write(f"Quartil 1 (Q1),{q1:.2f}\n")
                f.write(f"Quartil 3 (Q3),{q3:.2f}\n")
                f.write("\n") 

                # BLOCO 2: Dias da Semana (NOVO)
                f.write("=== ANALISE POR DIA DA SEMANA ===\n")
                f.write("Dia,Media,Qtd_Medicoes\n")
                for i in range(7):
                    if resumo_dias[i]:
                        m_dia, qtd_dia = resumo_dias[i]
                        f.write(f"{nomes_dias[i]},{m_dia:.2f},{qtd_dia}\n")
                    else:
                        f.write(f"{nomes_dias[i]},0,0\n")
                f.write("\n")

                # BLOCO 3: Análise Horária
                f.write("=== ANALISE DE PADRAO HORARIO ===\n")
                f.write("Hora,Media,Qtd_Medicoes,Minimo_Hora,Maximo_Hora\n")
                for h in range(24):
                    if resumo_horas[h]:
                        m_h, q_h, min_h, max_h = resumo_horas[h]
                        f.write(f"{h:02d}:00 - {h:02d}:59,{m_h:.2f},{q_h},{min_h},{max_h}\n")
                    else:
                        f.write(f"{h:02d}:00 - {h:02d}:59,0,0,0,0\n")

            print(f"Sucesso! Arquivo '{nome_arquivo}' criado.")
        
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
    else:
        print("Arquivo não foi gerado.")