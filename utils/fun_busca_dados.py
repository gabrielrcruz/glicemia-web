def realizar_busca_avancada(lista_dados):
    print("\n=== BUSCA AVANÇADA DE DADOS ===")
    print("Dica: Deixe em branco e aperte ENTER para ignorar um filtro.")

    # --- 1. Coleta de Filtros ---
    
    # Filtro de DATA
    inicio_data = input("Data Inicial (AAAA-MM-DD): ").strip()
    fim_data = input("Data Final   (AAAA-MM-DD): ").strip()

    # Filtro de VALOR
    min_valor = input("Valor Mínimo de Glicemia: ").strip()
    max_valor = input("Valor Máximo de Glicemia: ").strip()

    # Filtro de HORÁRIO (Apenas Hora cheia)
    inicio_hora = input("Hora Inicial (0-23): ").strip()
    fim_hora = input("Hora Final   (0-23): ").strip()

    print("\nProcessando busca...")

    resultados = []
    
    # --- 2. Processamento ---
    for linha in lista_dados[1:]: # Pula cabeçalho
        if len(linha) < 3: continue

        try:
            data_str = linha[0] # "2025-10-08"
            hora_str = linha[1] # "18:01:00"
            valor_str = linha[2]
            
            valor_float = float(valor_str)
            valor_int = int(valor_float)
            
            # Verifica DATA
            if inicio_data:
                if data_str < inicio_data: continue
            if fim_data:
                if data_str > fim_data: continue

            # Verifica VALOR
            if min_valor:
                if valor_int < int(min_valor): continue
            if max_valor:
                if valor_int > int(max_valor): continue

            # Verifica HORÁRIO
            # Extrai a hora cheia da string "18:01:00" -> 18
            h_atual = int(hora_str.split(':')[0])
            
            if inicio_hora:
                if h_atual < int(inicio_hora): continue
            if fim_hora:
                if h_atual > int(fim_hora): continue

            # Se passou por todos os "continue", é um match!
            resultados.append(linha)

        except ValueError:
            continue

    # --- 3. Exibição ---
    qtd = len(resultados)
    if qtd == 0:
        print("Nenhum registro encontrado com esses critérios.")
    else:
        print(f"\nForam encontrados {qtd} registros:")
        print("-" * 40)
        # Mostra os primeiros 10 para não poluir a tela, ou todos se for pouco
        limite_exibicao = 15
        for i, reg in enumerate(resultados):
            if i < limite_exibicao:
                print(f"Data: {reg[0]} | Hora: {reg[1]} | Valor: {reg[2]}")
            else:
                print(f"... e mais {qtd - limite_exibicao} registros.")
                break
        print("-" * 40)

        # --- 4. Salvar ---
        salvar = input("Deseja salvar esses resultados filtrados em CSV? (s/n): ")
        if salvar.lower() in ['s', 'sim']:
            nome_arq = input("Nome do arquivo: ")
            if not nome_arq.endswith('.csv'): nome_arq += '.csv'
            
            try:
                with open(nome_arq, 'w', encoding='utf-8') as f:
                    f.write("Data,Hora,Valor\n")
                    for r in resultados:
                        # Reconstrói a linha CSV
                        f.write(f"{r[0]},{r[1]},{r[2]}\n")
                print(f"Arquivo '{nome_arq}' salvo com sucesso!")
            except Exception as e:
                print(f"Erro ao salvar: {e}")