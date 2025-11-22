# utils/gerenciador_arquivo.py

def salvar_novas_medicoes(arquivo_destino, lista_novas_linhas):
    """
    Recebe o caminho do arquivo principal e uma lista de strings (linhas CSV)
    para adicionar ao final.
    """
    try:
        with open(arquivo_destino, 'a', encoding='utf-8') as f:
            # Garante que começa numa nova linha
            f.write('\n')
            
            count = 0
            for linha in lista_novas_linhas:
                # Limpeza básica
                linha_limpa = linha.strip()
                if len(linha_limpa) > 5: # Evita linhas vazias ou "lixo"
                    f.write(linha_limpa + '\n')
                    count += 1
        return True, count # Retorna Sucesso e qtd adicionada
    except Exception as e:
        return False, str(e)
    
# ... (mantenha a função salvar_novas_medicoes aqui em cima) ...

def excluir_registro_por_id(arquivo_csv, id_linha):
    """Lê tudo, remove a linha com aquele índice e salva tudo de novo."""
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        # Verifica se o ID é válido
        if id_linha < 1 or id_linha >= len(linhas):
            return False, "ID inválido."

        # Remove a linha específica da memória
        del linhas[id_linha]

        # Reescreve o arquivo
        with open(arquivo_csv, 'w', encoding='utf-8') as f:
            f.writelines(linhas)
            
        return True, "Registro excluído."
    except Exception as e:
        return False, str(e)

def atualizar_registro_por_id(arquivo_csv, id_linha, nova_data, nova_hora, novo_valor):
    """Substitui uma linha específica."""
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        if id_linha < 1 or id_linha >= len(linhas):
            return False, "ID inválido."
            
        # Monta a nova linha (mantendo o padrão CSV)
        nova_linha_str = f"{nova_data},{nova_hora},{novo_valor}\n"
        
        # Substitui na lista
        linhas[id_linha] = nova_linha_str
        
        # Salva
        with open(arquivo_csv, 'w', encoding='utf-8') as f:
            f.writelines(linhas)
            
        return True, "Registro atualizado."
    except Exception as e:
        return False, str(e)