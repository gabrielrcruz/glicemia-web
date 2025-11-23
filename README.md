# 🩸 Monitor de Glicemia (Glicemia App)

Este projeto é um sistema completo em **Python** para monitoramento, análise e gestão de dados de glicemia. Ele oferece ferramentas para importação de medições, análises estatísticas avançadas (como HbA1c estimada e variabilidade) e geração de relatórios.

O sistema é dividido em duas versões principais:
1.  **Projeto CLI:** Uma versão robusta para terminal.
2.  **Projeto Web:** Uma aplicação moderna construída com Flask e implantada na nuvem.

## 🌐 Demonstração Online
Acesse a versão web do projeto aqui:  
👉 **[https://glicemia-web-717914731379.southamerica-east1.run.app/](https://glicemia-web-717914731379.southamerica-east1.run.app/)**

---

## 🖥️ 1. Projeto CLI (Versão Terminal)

A versão de linha de comando está localizada na pasta `Projeto_CLI`. O sistema funciona através de um menu interativo que processa um arquivo CSV local (`dados_glicemia.csv`).

### Estrutura e Funcionalidades
O arquivo principal é o `app.py`, que orquestra as seguintes funções modulares:

* **`fun_info_arquivo.py`**:
    * Responsável por ler o arquivo bruto e exibir metadados essenciais, como cabeçalho, quantidade de colunas, total de registros e o intervalo de datas das medições.

* **`fun_arq_parcial.py`**:
    * Gera novos arquivos CSV filtrados baseados em critérios médicos:
        * **Hipoglicemia:** Filtra valores < 70 mg/dL.
        * **Hiperglicemia:** Filtra valores > 180 mg/dL.
        * **Alvo:** Filtra valores entre 70-150 mg/dL.
        * **Ordenação:** Cria um arquivo ordenado (crescente/decrescente) pelos valores de glicemia.

* **`fun_dados_agrupados.py`**:
    * Realiza cálculos clínicos e agrupamentos de dados:
        * **Tempo no Alvo (TIR):** Calcula a % de tempo em Hipo, Alvo e Hiper.
        * **HbA1c Estimada:** Aplica a fórmula ADAG para estimar a hemoglobina glicada baseada na média.
        * **Variabilidade (%CV):** Calcula o Desvio Padrão e o Coeficiente de Variação.
        * **Upload:** Permite anexar novos dados CSV ao arquivo principal.

* **`fun_dados_estatisticos.py`**:
    * Gera o "Relatório Master". Calcula média, mediana, quartis e desvio padrão.
    * **Análise de Padrões:** Identifica automaticamente quais dias da semana e faixas horárias apresentam as maiores e menores médias glicêmicas.

* **`fun_busca_dados.py`**:
    * Implementa um motor de busca avançada que permite filtrar simultaneamente por data (início/fim), valor (mín/máx) e hora.

* **`fun_interface.py`**:
    * Gerencia a exibição do menu principal e a navegação do usuário.

---

## ☁️ 2. Projeto Web (Flask & Cloud)

A versão web (`app_flask.py`) adapta a lógica do CLI para uma interface gráfica amigável, acessível via navegador.

### Detalhes da Implementação

#### **Arquitetura Backend**
* **Framework:** Utiliza **Flask** seguindo o padrão MVC.
* **Modularização (`utils/`):** A lógica de negócios foi separada das rotas. Módulos como `analises.py` e `filtros.py` são reutilizados para manter o código limpo.
* **Processamento de Arquivos:**
    * O módulo `processador_upload.py` utiliza `io.StringIO` e `datetime` para detectar e converter automaticamente diferentes formatos de data e codificações (UTF-8, Latin-1) durante o upload.
    * A exportação de CSVs (`exportacao.py`) é feita em memória, servindo o download diretamente ao usuário sem salvar arquivos temporários no servidor.

#### **Frontend**
* Utiliza **Jinja2** para renderizar templates HTML dinâmicos localizados na pasta `templates/`.
* Destaques visuais incluem cards de métricas com formatação condicional (cores para níveis de alerta) e tabelas responsivas.

#### **Deploy e Infraestrutura**
* **Docker:** A aplicação é conteinerizada usando um `Dockerfile` baseado na imagem `python:3.10-slim`.
* **Servidor WSGI:** Utiliza **Gunicorn** (configurado via `Procfile`) para garantir performance em produção.
* **Hospedagem:** O projeto está rodando no **Google Cloud Run**, permitindo escalabilidade automática.

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
* Python 3.10+
* Pip

### Instalação
1.  Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/glicemia-web.git](https://github.com/seu-usuario/glicemia-web.git)
    cd glicemia-web
    ```

2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Para rodar a versão Web:**
    ```bash
    python app_flask.py
    ```
    Acesse em `http://localhost:5000`

4.  **Para rodar a versão CLI:**
    ```bash
    cd Projeto_CLI
    python app.py
    ```

---

Desenvolvido por Gabriel Cruz.
