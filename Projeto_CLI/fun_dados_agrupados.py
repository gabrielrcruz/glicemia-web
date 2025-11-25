from fun_interface import exibir_menu



def dados_agrupados(lista_dados):

    def menu_dados_agrupados():
        print("\n--- Menu de informações Parciais---")
        print("1. Tempo no Alvo (Time in Range - TIR)")
        print("2. Estimativa de HbA1c (Hemoglobina Glicada)")
        print("3. Variabilidade Glicêmica")
        print("4. Media Total")
        print("5. Fazer Upload de Medições")
        print("6. Voltar a menu Anterior")
        print("---------------------")
    
    while True:
            
            menu_dados_agrupados()
            escolha = input("Digite sua escolha: ")
            
            if escolha == '1':
                print("1. Tempo no Alvo (Time in Range - TIR)")

                def gerar_tempo_no_alvo(lista_dados):
                    print("\n--- [Relatório] Tempo no Alvo (Time in Range) ---")
                    print("O ideal é manter o tempo no alvo acima de 70%.")
                    
                    nome_arquivo = input("Nome do arquivo para salvar (ex: relatorio_tir): ")
                    if not nome_arquivo.endswith('.csv'):
                        nome_arquivo += '.csv'

                    # Contadores
                    qtd_hipo = 0    # < 70
                    qtd_alvo = 0    # 70 a 180
                    qtd_hiper = 0   # > 180
                    total_validos = 0

                    # Pular o cabeçalho e processar os dados
                    # lista_dados[1:] pega da segunda linha até o final
                    for linha in lista_dados[1:]:
                        # Verifica se a linha tem as 3 colunas (Data, Hora, Valor)
                        if len(linha) < 3:
                            continue
                            
                        try:
                            # Converte o valor da coluna 2 para número
                            valor = int(float(linha[2]))
                            total_validos += 1
                            
                            # Classificação
                            if valor < 70:
                                qtd_hipo += 1
                            elif 70 <= valor <= 180:
                                qtd_alvo += 1
                            else:
                                qtd_hiper += 1
                                
                        except ValueError:
                            continue # Pula linhas com erro

                    if total_validos == 0:
                        print("Não foram encontrados dados válidos para calcular.")
                        return

                    # Cálculo das porcentagens
                    perc_hipo = (qtd_hipo / total_validos) * 100
                    perc_alvo = (qtd_alvo / total_validos) * 100
                    perc_hiper = (qtd_hiper / total_validos) * 100

                    # Salvar no arquivo CSV
                    try:
                        with open(nome_arquivo, 'w', encoding='utf-8') as f:
                            f.write("Categoria,Quantidade,Porcentagem\n")
                            f.write(f"Hipoglicemia (<70 mg/dL),{qtd_hipo},{perc_hipo:.2f}%\n")
                            f.write(f"No Alvo (70-180 mg/dL),{qtd_alvo},{perc_alvo:.2f}%\n")
                            f.write(f"Hiperglicemia (>180 mg/dL),{qtd_hiper},{perc_hiper:.2f}%\n")
                            f.write(f"TOTAL,{total_validos},100%\n")

                        print(f"\nSucesso! Arquivo '{nome_arquivo}' gerado.")
                        print(f"Resumo rápido:")
                        print(f" -> Hipo: {perc_hipo:.1f}%")
                        print(f" -> Alvo: {perc_alvo:.1f}%")
                        print(f" -> Hiper: {perc_hiper:.1f}%")

                    except Exception as e:
                        print(f"Erro ao salvar o arquivo: {e}")
                gerar_tempo_no_alvo(lista_dados)
            elif escolha == '2':
                print("Escolha 2")
                def gerar_estimativa_hba1c(lista_dados):
                    print("\n--- [Relatório] Estimativa de HbA1c (Glicada) ---")
                    print("Nota: Este cálculo é uma estimativa baseada na média das medições.")
                    
                    nome_arquivo = input("Nome do arquivo para salvar (ex: estimativa_a1c): ")
                    if not nome_arquivo.endswith('.csv'):
                        nome_arquivo += '.csv'

                    soma_glicemia = 0
                    total_validos = 0

                    # 1. Calcular a Média Geral
                    for linha in lista_dados[1:]:
                        if len(linha) < 3: continue
                        try:
                            valor = int(float(linha[2]))
                            soma_glicemia += valor
                            total_validos += 1
                        except ValueError:
                            continue

                    if total_validos == 0:
                        print("Sem dados suficientes para calcular.")
                        return

                    media_geral = soma_glicemia / total_validos
                    
                    # 2. Aplicar a Fórmula ADAG
                    # HbA1c = (Média + 46.7) / 28.7
                    hba1c_estimada = (media_geral + 46.7) / 28.7

                    try:
                        with open(nome_arquivo, 'w', encoding='utf-8') as f:
                            f.write("Indicador,Valor\n")
                            f.write(f"Media Geral de Glicemia,{media_geral:.2f}\n")
                            f.write(f"Hemoglobina Glicada Estimada (HbA1c),{hba1c_estimada:.2f}%\n")
                            f.write(f"Total de medicoes consideradas,{total_validos}\n")
                            
                        print(f"\nSucesso! Arquivo '{nome_arquivo}' gerado.")
                        print(f"Sua Média Geral: {media_geral:.0f} mg/dL")
                        print(f"Sua HbA1c Estimada: {hba1c_estimada:.1f}%")
                        
                    except Exception as e:
                        print(f"Erro ao salvar: {e}")

                gerar_estimativa_hba1c(lista_dados)
            elif escolha == '3':
                import math 
                print("Escolha 3")
                def gerar_variabilidade(lista_dados):
                    print("\n--- [Relatório] Variabilidade Glicêmica (%CV) ---")
                    print("Mede a oscilação da glicose. Ideal: < 36%")

                    nome_arquivo = input("Nome do arquivo para salvar (ex: variabilidade): ")
                    if not nome_arquivo.endswith('.csv'):
                        nome_arquivo += '.csv'

                    # 1. Extrair todos os valores válidos para uma lista numérica
                    valores_validos = []
                    
                    for linha in lista_dados[1:]:
                        if len(linha) < 3: continue
                        try:
                            valor = int(float(linha[2]))
                            valores_validos.append(valor)
                        except ValueError:
                            continue

                    qtd = len(valores_validos)
                    if qtd < 2:
                        print("Dados insuficientes para cálculo de desvio padrão (mínimo 2).")
                        return

                    # 2. Calcular Média
                    media = sum(valores_validos) / qtd

                    # 3. Calcular Desvio Padrão (Standard Deviation)
                    # Fórmula: Raiz Quadrada da (Soma das diferenças ao quadrado / N-1)
                    soma_diferencas_quadrado = sum((x - media) ** 2 for x in valores_validos)
                    variancia = soma_diferencas_quadrado / (qtd - 1)
                    desvio_padrao = math.sqrt(variancia)

                    # 4. Calcular Coeficiente de Variação (%CV)
                    # Fórmula: (Desvio Padrão / Média) * 100
                    coeficiente_variacao = (desvio_padrao / media) * 100

                    # Classificação simples
                    status = "Estável" if coeficiente_variacao < 36 else "Instável (Oscilando muito)"

                    try:
                        with open(nome_arquivo, 'w', encoding='utf-8') as f:
                            f.write("Indicador,Valor,Status\n")
                            f.write(f"Media Glicemica,{media:.2f},-\n")
                            f.write(f"Desvio Padrao (SD),{desvio_padrao:.2f},-\n")
                            f.write(f"Variabilidade (%CV),{coeficiente_variacao:.2f}%,{status}\n")
                            
                        print(f"\nSucesso! Arquivo '{nome_arquivo}' gerado.")
                        print(f"Desvio Padrão: {desvio_padrao:.1f}")
                        print(f"Variabilidade (%CV): {coeficiente_variacao:.1f}% -> {status}")

                    except Exception as e:
                        print(f"Erro ao salvar: {e}")
                gerar_variabilidade(lista_dados)
            elif escolha == '4':
                print("Escolha 4")
                def gerar_frequencia_diaria(lista_dados):
                    print("\n--- [Relatório] Frequência de Medições Diárias ---")
                    print("Analisa quantos testes foram feitos em cada dia.")
                    
                    nome_arquivo = input("Nome do arquivo para salvar (ex: frequencia_diaria): ")
                    if not nome_arquivo.endswith('.csv'):
                        nome_arquivo += '.csv'

                    # Dicionário para contar: {'2025-10-08': 5, '2025-10-09': 3}
                    contagem_dias = {}
                    total_geral = 0

                    # Ignora cabeçalho
                    for linha in lista_dados[1:]:
                        if len(linha) < 3: continue
                        
                        # Pega a data (Coluna 0)
                        data = linha[0]
                        
                        # Validamos se a coluna valor é numérica para garantir que é um registro válido
                        try:
                            float(linha[2])
                            
                            # Se a data já existe, soma +1, se não, começa com 1
                            if data in contagem_dias:
                                contagem_dias[data] += 1
                            else:
                                contagem_dias[data] = 1
                                
                            total_geral += 1
                            
                        except ValueError:
                            continue # Pula linhas inválidas

                    if total_geral == 0:
                        print("Nenhum dado válido encontrado.")
                        return

                    try:
                        with open(nome_arquivo, 'w', encoding='utf-8') as f:
                            f.write("Data,Qtd_Testes,Porcentagem_do_Total\n")
                            
                            # Ordena as datas para ficar bonito no CSV
                            for data in sorted(contagem_dias.keys()):
                                qtd = contagem_dias[data]
                                porcentagem = (qtd / total_geral) * 100
                                
                                f.write(f"{data},{qtd},{porcentagem:.2f}%\n")
                            
                            # Adiciona uma linha final de totalização
                            f.write(f"TOTAL_GERAL,{total_geral},100%\n")

                        print(f"\nSucesso! Arquivo '{nome_arquivo}' gerado.")
                        print(f"Total de medições analisadas: {total_geral}")
                        print(f"Dias monitorados: {len(contagem_dias)}")

                    except Exception as e:
                        print(f"Erro ao salvar: {e}")
                gerar_frequencia_diaria(lista_dados)
                
            elif escolha == '5':
                print("Escolha 5")
                def adicionar_medicoes(arquivo_principal):
                    print("\n--- Upload de Novas Medições ---")
                    print(f"Arquivo de destino: {arquivo_principal}")
                    
                    # 1. Pedir o nome do arquivo que contem os novos dados
                    arquivo_novos_dados = input("Digite o nome do arquivo CSV com as novas medições: ")
                    
                    if not arquivo_novos_dados.endswith('.csv'):
                        arquivo_novos_dados += '.csv'

                    try:
                        # 2. Ler os novos dados
                        with open(arquivo_novos_dados, 'r', encoding='utf-8') as f_origem:
                            linhas_novas = f_origem.readlines()
                            
                        if len(linhas_novas) == 0:
                            print("O arquivo de origem está vazio.")
                            return

                        # 3. Verificar e remover cabeçalho dos novos dados
                        # Se a primeira linha tiver "Data" ou "Valor", assumimos que é cabeçalho
                        if "Data" in linhas_novas[0] or "Valor" in linhas_novas[0]:
                            dados_para_adicionar = linhas_novas[1:]
                        else:
                            dados_para_adicionar = linhas_novas

                        count = 0
                        
                        # 4. Adicionar ao arquivo principal (Modo 'a' = Append/Anexar)
                        with open(arquivo_principal, 'a', encoding='utf-8') as f_destino:
                            # Garante uma quebra de linha antes de começar, para não grudar 
                            # na última medição se o arquivo não tiver terminado com enter
                            f_destino.write('\n')
                            
                            for linha in dados_para_adicionar:
                                # Remove espaços em branco extras e verifica se tem conteúdo
                                if len(linha.strip()) > 5: 
                                    f_destino.write(linha.strip() + '\n')
                                    count += 1

                        print(f"\nSucesso! {count} novas medições foram adicionadas ao final de '{arquivo_principal}'.")
                        print("Recomendamos reiniciar o programa para carregar os novos dados na memória.")

                    except FileNotFoundError:
                        print(f"Erro: O arquivo '{arquivo_novos_dados}' não foi encontrado.")
                    except Exception as e:
                        print(f"Erro ao atualizar arquivo: {e}")
                adicionar_medicoes("dados_glicemia.csv")
            elif escolha == '6':
                print("Voltando ao menu Anterior")
                exibir_menu()
                break  # Sai do loop while
            else:
                print("Opção inválida. Tente novamente.")





                    


