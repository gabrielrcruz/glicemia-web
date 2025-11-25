
#função que exibi as informações do arquivo
from fun_info_arquivo import inf_arquivo

#função que cria as informações parciais
from fun_arq_parcial import parcial_arq

#função que gera dados agrupados
from fun_dados_agrupados import dados_agrupados

#função que exibe o menu
from fun_interface import exibir_menu

#função de dados estatisticos
from fun_dados_estatisticos import gerar_relatorio_completo

#função que faz a busca de dados 
from fun_busca_dados import realizar_busca_avancada


#função que vai fazer o csv virar uma lista
dados_limpos = inf_arquivo("dados_glicemia.csv")


def menu_principal():
    """Loop principal que gerencia o menu."""
    
    while True:
        exibir_menu()
        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            print("Você escolheu exibir informações do Arquivo")
            print("Cabeçalho:", dados_limpos[0])
            print("Quantidade de Colunas", len(dados_limpos[0]))
            print("Quantidade de Medições", len(dados_limpos) - 1)
            print("Primeira medição:", dados_limpos[1])
            print("Ultima Medição:", dados_limpos[-1])
        elif escolha == '2':
            parcial_arq(dados_limpos)
        elif escolha == '3':
            dados_agrupados(dados_limpos)
        elif escolha == '4':
            gerar_relatorio_completo(dados_limpos)
        elif escolha == '5':
            print("Atenção! Seus dados vão de", dados_limpos[1][0] , "Até a data de" ,dados_limpos[-1][0])
            realizar_busca_avancada(dados_limpos)
        elif escolha == '6':
            print("Finalizando o programa. Até mais!")
            break  # Sai do loop while
        else:
            print("Opção inválida. Tente novamente.")



if __name__ == "__main__":
    menu_principal()