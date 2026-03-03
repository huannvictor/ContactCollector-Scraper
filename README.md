# Info Escolas — Coletor Luz do Saber

Este projeto automatiza a extração de dados de contato das escolas na plataforma **Luz do Saber**.

## 🎯 Desafio

### Problemática

No exercício da minha função como **Assistente Comercial**, identifiquei um gargalo operacional crítico: a necessidade de preencher planilhas de atualização cadastral com contatos (telefones e e-mails) de diretores escolares.

O sistema legado da empresa não oferecia relatórios exportáveis com esses dados consolidados. O processo exigia que um colaborador acessasse manualmente o perfil de cada escola, localizasse as informações e as transferisse via "copiar e colar" para o Excel. Esse método era:

* **Altamente ineficiente:** Consumia horas valiosas de trabalho humano em tarefas repetitivas.
* **Propenso a erros:** A fadiga humana aumentava o risco de falhas na digitação ou omissão de dados.
* **Inconsistente:** A falta de padronização nos campos de telefone do sistema dificultava a organização posterior.

### Solução

Desenvolvi um robô de **RPA (Robotic Process Automation)** em Python para assumir essa tarefa de ponta a ponta:

* **Extração Inteligente:** Utilizando **Playwright**, o script automatiza o fluxo de login e navegação, processando uma lista de IDs fornecida via arquivo texto.
* **Sanitização de Dados:** Implementei algoritmos de **Regex** para tratar a variabilidade dos dados (telefones fixos, celulares com 8 ou 9 dígitos, DDDs e e-mails), garantindo que a saída seja sempre padronizada e profissional.
* **Arquitetura Escalável:** O projeto segue padrões de engenharia de software (*The Blueprint*), com separação clara entre lógica de negócio, utilitários e gestão de dados, além de uma camada de segurança para proteção de credenciais.
* **Resultados Tangíveis:** O que antes levava horas agora é concluído em minutos, com 100% de precisão e geração automática de um relatório final em Excel.

## 🛠️ Desenvolvimento e Tecnologias

Este projeto foi concebido e arquitetado por mim, utilizando uma abordagem de **Desenvolvimento Orientado a IA**. Para a implementação técnica, utilizei o **Gemini CLI** como parceiro de *pair programming*.

### Por que essa abordagem?
A escolha de utilizar IA no desenvolvimento reflete minha habilidade em:
*   **Visão de Produto:** Identificar oportunidades de automação e definir requisitos claros.
*   **Direcionamento Técnico:** Orquestrar ferramentas complexas como Playwright, Pandas e Regex para resolver problemas reais de negócio.
*   **Eficiência e Qualidade:** Entregar uma solução com arquitetura profissional (*The Blueprint*), segurança e documentação impecável em tempo recorde.

Embora eu não seja um especialista profundo em todas as sintaxes de cada biblioteca utilizada, possuo o **domínio dos conceitos de engenharia** necessários para guiar a IA na construção de uma ferramenta robusta, escalável e pronta para produção.

## 🏗️ Estrutura do Projeto (The Blueprint)

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

* Copie o arquivo `.env.example` para um novo arquivo chamado `.env`.
* Abra o arquivo `.env` e preencha com seus dados:

  ```.env
  LUZ_USER=seu_usuario
  LUZ_PASS=sua_senha
  LUZ_BASE_URL=https://...
  LUZ_LOGIN_URL=https://...
  LUZ_SCHOOL_URL_PREFIX=https://...
  ```

  *Obs: O arquivo `.env` é ignorado pelo Git por segurança.*

1. Coloque os códigos das escolas em `data/input/codigos.txt`.
2. Execute o script:

* No Windows: Use o arquivo `scripts/run.bat`
* No terminal: `python -m src.main`

## Amostra de Resultado (Output)

Abaixo, um exemplo de como os dados são extraídos e organizados na planilha final:

| fixo | celular | celular_diretor | nome_do_administrador_legal | email | codigo_escola | erro |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| (11) 4002-8922 | 98877-6655 | 98877-6655 | João da Silva | contato@escola-exemplo.com.br | 12345 | |
| (21) 3344-5566 | 91122-3344 | 95566-7788 | Maria Oliveira | secretaria@colegio-modelo.edu.br | 67890 | |
| | 99988-7766 | 99988-7766 | Carlos Souza | direcao@instituto-exemplo.org | 11223 | timeout |

> Você pode baixar o arquivo completo de exemplo em: [`samples/exemplo_resultado.xlsx`](samples/exemplo_resultado.xlsx)

## Requisitos

* Python 3.8+
* Bibliotecas: Playwright, Pandas, Openpyxl, Python-dotenv.
