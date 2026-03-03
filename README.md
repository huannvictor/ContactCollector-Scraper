# Info Escolas — Coletor Luz do Saber

Este projeto automatiza a extração de dados de contato das escolas na plataforma **Luz do Saber**.

## Estrutura do Projeto (The Blueprint)

```text
info-escolas/
├── data/                   # Gestão de arquivos
│   ├── input/              # Arquivos de entrada
│   │   ├── ref/            # Planilhas base e snapshots técnicos
│   │   └── codigos.txt     # IDs das escolas para processamento
│   └── output/             # Resultados gerados (Excel)
├── logs/                   # Histórico de execução para auditoria
├── scripts/                # Facilitadores (run.bat)
├── src/                    # O Coração (Código-fonte)
│   ├── __init__.py
│   ├── core.py             # Lógica principal (Regex e extração)
│   ├── main.py             # Ponto de entrada (Orquestrador)
│   └── utils.py            # Ferramentas de apoio (Logs, formatadores)
├── tests/                  # Testes unitários
├── .env                    # Credenciais (Arquivo privado)
├── .gitignore              # Proteção de arquivos sensíveis
├── README.md               # Documentação
└── requirements.txt        # Lista de dependências
```

## Como Usar

1. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    playwright install chromium
    ```

2. **Configure suas credenciais e URLs:**
    - Copie o arquivo `.env.example` para um novo arquivo chamado `.env`.
    - Abra o arquivo `.env` e preencha com seus dados:
    ```text
    LUZ_USER=seu_usuario
    LUZ_PASS=sua_senha
    LUZ_BASE_URL=https://...
    LUZ_LOGIN_URL=https://...
    LUZ_SCHOOL_URL_PREFIX=https://...
    ```
    *Obs: O arquivo `.env` é ignorado pelo Git por segurança.*

3. Coloque os códigos das escolas em `data/input/codigos.txt`.
4. Execute o script:
    - No Windows: Use o arquivo `scripts/run.bat`
    - No terminal: `python -m src.main`

## Amostra de Resultado (Output)

Abaixo, um exemplo de como os dados são extraídos e organizados na planilha final:

| fixo | celular | celular_diretor | nome_do_administrador_legal | email | codigo_escola | erro |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| (11) 4002-8922 | 98877-6655 | 98877-6655 | João da Silva | contato@escola-exemplo.com.br | 12345 | |
| (21) 3344-5566 | 91122-3344 | 95566-7788 | Maria Oliveira | secretaria@colegio-modelo.edu.br | 67890 | |
| | 99988-7766 | 99988-7766 | Carlos Souza | direcao@instituto-exemplo.org | 11223 | timeout |

> Você pode baixar o arquivo completo de exemplo em: [`samples/exemplo_resultado.xlsx`](samples/exemplo_resultado.xlsx)

## Requisitos

- Python 3.8+
- Bibliotecas: Playwright, Pandas, Openpyxl, Python-dotenv.
