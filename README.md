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

2. **Configure suas credenciais:**
    - Copie o arquivo `.env.example` para um novo arquivo chamado `.env`.
    - Abra o arquivo `.env` e preencha com seu usuário e senha:

    ```text
    LUZ_USER=seu_usuario
    LUZ_PASS=sua_senha
    ```

    *Obs: O arquivo `.env` é ignorado pelo Git por segurança.*

3. Coloque os códigos das escolas em `data/input/codigos.txt`.
4. Execute o script:
    - No Windows: Use o arquivo `scripts/run.bat`
    - No terminal: `python -m src.main`

## Requisitos

- Python 3.8+
- Bibliotecas: Playwright, Pandas, Openpyxl, Python-dotenv.
