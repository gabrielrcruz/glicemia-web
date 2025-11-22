import math

# --- 1. Tempo no Alvo (TIR) ---
def calcular_tempo_no_alvo(lista_dados):
    hipo = 0
    alvo = 0
    hiper = 0
    total = 0
    
    # Começa do índice 1 para pular o cabeçalho
    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        try:
            valor = float(linha[2])
            total += 1
            if valor < 70:
                hipo += 1
            elif 70 <= valor <= 180:
                alvo += 1
            else:
                hiper += 1
        except ValueError:
            continue
            
    if total == 0: return None

    return {
        "hipo_pct": round((hipo / total) * 100, 1),
        "alvo_pct": round((alvo / total) * 100, 1),
        "hiper_pct": round((hiper / total) * 100, 1),
        "total_registros": total
    }

# --- 2. HbA1c Estimada (A que estava faltando) ---
def calcular_hba1c_estimada(lista_dados):
    soma = 0
    total = 0
    
    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        try:
            valor = float(linha[2])
            soma += valor
            total += 1
        except ValueError:
            continue
            
    if total == 0: return 0
    
    media = soma / total
    # Fórmula ADAG: (Média + 46.7) / 28.7
    hba1c = (media + 46.7) / 28.7
    return round(hba1c, 1)

# --- 3. Variabilidade (%CV) ---
def calcular_variabilidade(lista_dados):
    valores = []
    for linha in lista_dados[1:]:
        if len(linha) < 3: continue
        try:
            valores.append(float(linha[2]))
        except ValueError: continue
            
    if len(valores) < 2: return None
    
    media = sum(valores) / len(valores)
    
    # Variância e Desvio Padrão
    variancia = sum((x - media) ** 2 for x in valores) / (len(valores) - 1)
    desvio = math.sqrt(variancia)
    
    if media == 0: return None # Evita divisão por zero
    
    cv = (desvio / media) * 100
    
    status = "Estável" if cv < 36 else "Instável"
    
    return {
        "cv": round(cv, 1),
        "desvio": round(desvio, 1),
        "status": status
    }