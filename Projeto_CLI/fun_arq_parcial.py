from fun_interface import exibir_menu



def parcial_arq(dados):

    def menu_arquivo_parcial():
        print("\n--- Menu de informações Parciais---")
        print("1. Arquivo com valores de Hipoglicemia")
        print("2. Arquivo com valores de Hiperglicemia")
        print("3. Arquivos com valores normais")
        print("4. Ordenar o Arquivo Valores Ordem Decrecente")
        print("5. Agrupar média Diária")
        print("6. Voltar a menu Anterior")
        print("---------------------")
    
    while True:
            from app import dados_limpos
            menu_arquivo_parcial()
            escolha = input("Digite sua escolha: ")
            
            if escolha == '1':

                print("Escolha 1")
                nome_arquivo = input("Qual nome você quer dar ao arquivo? (ex: alerta_hipo): ")
                def salvar_hipoglicemia_da_lista(dados, nome_arquivo):
                        print("--- Exportar Lista para CSV ---")
                        
                        if not nome_arquivo.endswith('.csv'):
                            nome_arquivo += '.csv'
                            
                        try:
                            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                                
                                f.write("Data,Hora,Valor\n")
                                
                                contador = 0
                                
                                for linha in dados:
                                    # Verificação de segurança: a linha tem as 3 colunas?
                                    if len(linha) < 3:
                                        continue

                                    data = linha[0]
                                    hora = linha[1]
                                    valor_bruto = linha[2] 
                                    
                                    
                                    try:
                                        # Tenta forçar a conversão para número ANTES de comparar
                                        # O float garante que funcione mesmo se vier "68.0" ou string "68"
                                        valor_numerico = int(float(valor_bruto))
                                        
                                        # Agora comparamos Número com Número
                                        if valor_numerico < 70: 
                                            f.write(f"{data},{hora},{valor_numerico}\n")
                                            contador += 1
                                    
                                    except ValueError:
                                        continue
                                        
                            print(f"\nSucesso! Arquivo '{nome_arquivo}' criado.")
                            print(f"Foram salvas {contador} linhas filtradas.")
                            
                        except Exception as e:
                            print(f"Ocorreu um erro: {e}")

                
                salvar_hipoglicemia_da_lista(dados, nome_arquivo)


            elif escolha == '2':
                print("Escolha 2")
                nome_arquivo = input("Qual nome você quer dar ao arquivo? (ex: alerta_hiper): ")
                def salvar_hiperglicemia(dados, nome_arquivo):
                        print("--- Exportar Lista para CSV ---")
                        
                        if not nome_arquivo.endswith('.csv'):
                            nome_arquivo += '.csv'
                            
                        try:
                            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                                
                                f.write("Data,Hora,Valor\n")
                                
                                contador = 0
                                
                                for linha in dados:
                                    # Verificação de segurança: a linha tem as 3 colunas?
                                    if len(linha) < 3:
                                        continue

                                    data = linha[0]
                                    hora = linha[1]
                                    valor_bruto = linha[2] 
                                    
                                    
                                    try:
                                        # Tenta forçar a conversão para número ANTES de comparar
                                        # O float garante que funcione mesmo se vier "68.0" ou string "68"
                                        valor_numerico = int(float(valor_bruto))
                                        
                                        # Agora comparamos Número com Número
                                        if valor_numerico > 180: 
                                            f.write(f"{data},{hora},{valor_numerico}\n")
                                            contador += 1
                                    
                                    except ValueError:
                                        continue
                                        
                            print(f"\nSucesso! Arquivo '{nome_arquivo}' criado.")
                            print(f"Foram salvas {contador} linhas filtradas.")
                            
                        except Exception as e:
                            print(f"Ocorreu um erro: {e}")

                
                salvar_hiperglicemia(dados, nome_arquivo)

                    

            elif escolha == '3':
                print("Escolha 3 - Arquivos com valores no alvo de Glicemia")
                nome_arquivo = input("Qual nome você quer dar ao arquivo? (ex: valores no alvo): ")
                def salvar_valor_alvo(dados, nome_arquivo):
                        print("--- Exportar Lista para CSV ---")
                        
                        if not nome_arquivo.endswith('.csv'):
                            nome_arquivo += '.csv'
                            
                        try:
                            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                                
                                f.write("Data,Hora,Valor\n")
                                
                                contador = 0
                                
                                for linha in dados:
                                    # Verificação de segurança: a linha tem as 3 colunas?
                                    if len(linha) < 3:
                                        continue

                                    data = linha[0]
                                    hora = linha[1]
                                    valor_bruto = linha[2] 
                                    
                                    
                                    try:
                                        # Tenta forçar a conversão para número ANTES de comparar
                                        # O float garante que funcione mesmo se vier "68.0" ou string "68"
                                        valor_numerico = int(float(valor_bruto))
                                        
                                        # Agora comparamos Número com Número
                                        if valor_numerico > 70 and valor_numerico < 150: 
                                            f.write(f"{data},{hora},{valor_numerico}\n")
                                            contador += 1
                                    
                                    except ValueError:
                                        continue
                                        
                            print(f"\nSucesso! Arquivo '{nome_arquivo}' criado.")
                            print(f"Foram salvas {contador} linhas filtradas.")
                            
                        except Exception as e:
                            print(f"Ocorreu um erro: {e}")

                
                salvar_valor_alvo(dados, nome_arquivo)

            elif escolha == '4':
                print("Escolha 4")
                print("Opção 4: Ordenar Glicemia (Decrescente)")
                nome_arquivo = input("Escolha um nome do Arquivo: ")

                def ordenar_decrescente(dados, nome_arquivo):
                    print("--- Ordenando por Valor ---")

                    # 1. Garante extensão .csv
                    if not nome_arquivo.endswith('.csv'):
                        nome_arquivo += '.csv'

                    # 2. Separa o cabeçalho (para ele não entrar na ordenação)
                    cabecalho = dados[0]
                    conteudo = dados[1:]

                    # 3. Limpeza rápida: remove linhas vazias ou quebradas antes de ordenar
                    conteudo_valido = []
                    for linha in conteudo:
                        if len(linha) >= 3:
                            # Verifica se a coluna 2 é realmente um número
                            try:
                                float(linha[2]) 
                                conteudo_valido.append(linha)
                            except ValueError:
                                continue # Pula linha com erro

                    # 4. A ORDENAÇÃO (O "Reverse" na coluna 2)
                    # key=lambda x: float(x[2]) -> Diz pro Python olhar só a coluna 2 e tratar como número
                    # reverse=True -> Do maior para o menor
                    conteudo_valido.sort(key=lambda x: float(x[2]), reverse=False)

                    # 5. Salvar
                    try:
                        with open(nome_arquivo, 'w', encoding='utf-8') as f:
                            # Reconstrói o cabeçalho: ['Data','Hora','Valor'] vira "Data,Hora,Valor"
                            f.write(','.join(cabecalho).strip() + '\n')

                            for linha in conteudo_valido:
                                # Reconstrói a linha
                                linha_str = f"{linha[0]},{linha[1]},{linha[2]}"
                                f.write(linha_str + '\n')
                        
                        print(f"Sucesso! Arquivo '{nome_arquivo}' gerado com os menores valores no topo.")

                    except Exception as e:
                        print(f"Erro ao salvar: {e}")

                
                
                # Chama a função
                ordenar_decrescente(dados, nome_arquivo)

            elif escolha == '5':
                print("Escolha 5")
                print("--- Gerando Resumo de Média Diária ---")
                nome_arquivo = input("Nome do arquivo para salvar o resumo: ")
                def gerar_media_diaria(lista_dados, nome_arquivo):
                    
                    # 1. Pedir nome do arquivo
                    if not nome_arquivo.endswith('.csv'):
                        nome_arquivo += '.csv'

                    # Dicionário para agrupar: {'2025-10-08': [161, 218], '2025-10-09': [210, 200...]}
                    agrupamento = {}

                    # Pular cabeçalho (começa do índice 1)
                    dados_reais = lista_dados[1:]

                    # 2. Loop para agrupar os valores por data
                    for linha in dados_reais:
                        if len(linha) < 3: continue

                        data = linha[0]
                        valor_bruto = linha[2]

                        try:
                            valor_numerico = int(float(valor_bruto))
                            
                            # Se a data ainda não está no dicionário, cria uma lista vazia pra ela
                            if data not in agrupamento:
                                agrupamento[data] = []
                            
                            # Adiciona o valor na lista daquela data
                            agrupamento[data].append(valor_numerico)

                        except ValueError:
                            continue # Pula sujeira

                    # 3. Calcular médias e Salvar
                    try:
                        with open(nome_arquivo, 'w', encoding='utf-8') as f:
                            # Escreve cabeçalho
                            f.write("Data,Media_Diaria,Qtd_Medicoes\n")
                            
                            # Itera sobre cada data encontrada (ordenada)
                            for data in sorted(agrupamento.keys()):
                                lista_valores = agrupamento[data]
                                
                                # CÁLCULO DA MÉDIA
                                soma = sum(lista_valores)
                                qtd = len(lista_valores)
                                media = soma / qtd
                                
                                # Formata a média com 2 casas decimais (.2f)
                                linha_csv = f"{data},{media:.2f},{qtd}\n"
                                f.write(linha_csv)

                        print(f"Sucesso! Resumo salvo em '{nome_arquivo}'.")
                        print(f"Foram processados {len(agrupamento)} dias diferentes.")

                    except Exception as e:
                        print(f"Erro ao salvar resumo: {e}")
                gerar_media_diaria(dados, nome_arquivo)    

                
            elif escolha == '6':
                print("Voltando ao menu Anterior")
                exibir_menu()
                break  # Sai do loop while
            else:
                print("Opção inválida. Tente novamente.")





                    


