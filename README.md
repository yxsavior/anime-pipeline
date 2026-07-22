# Anime Pipeline
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

Pipeline de Engenharia de Dados desenvolvido em Python para ingestão, transformação, validação e carga de dados da Tenrai API em PostgreSQL, seguindo uma arquitetura em camadas Bronze, Silver e Gold.

> **Nota:** O projeto foi iniciado utilizando a Jikan API. Durante o desenvolvimento, a fonte foi substituída pela Tenrai API devido à indisponibilidade da Jikan. O notebook `api_exploration.ipynb` e o documento `source_analysis.md` ainda serão atualizados para refletir essa mudança. Essa pendência é apenas documental.

## Arquitetura

```text
┌────────────┐
│ Tenrai API │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Bronze     │
│ Raw JSON   │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Transform  │
│ Validation │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Silver     │
│ PostgreSQL │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ Gold       │
│ Analytics  │
└────────────┘
```

## Funcionalidades implementadas

* Consumo paginado da Tenrai API
* Armazenamento dos dados brutos (Bronze)
* Modelagem relacional
* Transformação dos dados
* Validação de qualidade
* Persistência intermediária em JSON
* Carga no PostgreSQL (Silver)

## Tecnologias

* Python
* PostgreSQL
* SQL
* Docker
* Requests
* psycopg

## Estrutura do projeto

```text
anime-pipeline/
│
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore
├── README.md
├── docker-compose.yml        # Serviços Docker
├── pyproject.toml            # Configuração do projeto
│
├── data/
│   ├── raw/                  # Dados brutos da API (por data)
│   └── processed/            # Dados transformados (por data)
│
├── docs/
│   ├── data_dictionary.md      # Dicionário de dados
│   └── source_analysis.md      # Análise da API e da fonte de dados
│
├── notebooks/
│   └── api_exploration.ipynb   # Exploração da API
│
├── sql/
│   └── schema.sql
│
├── src/
│   ├── main.py
│   ├── config.py
│   │
│   ├── ingestion/
│   │   ├── api_client.py
│   │   └── extract.py
│   │
│   ├── transformation/
│   │   ├── transform.py
│   │   └── validation.py
│   │
│   ├── loading/
│   │   ├── prepare.py
│   │   └── postgres.py
│   │
│   └── utils/
│       └── storage.py
│
└── tests/
    └── test_db.py
```

## Execução
| Etapa                          | Comando                                                 |
| ------------------------------ | --------------------------------------------------------|
| Clonar repositório             | `git clone git@github.com:yxsavior/anime-pipeline.git`  |
| Criar ambiente virtual         | `python -m venv .venv`                                  |
| Ativar ambiente (Windows)      | `.venv\Scripts\activate`                                |
| Ativar ambiente (Linux/macOS)  | `source .venv/bin/activate`                             |
| Instalar dependências          | `pip install -e .`                                      |
| Configurar variáveis ambiente  | `cp .env.example .env`                                  |
| Subir PostgreSQL               | `docker compose up -d`                                  |
| Executar pipeline              | `python -m src.main`                                    |

> O projeto possui uma dependência opcional para notebooks de exploração da fonte de dados (`api_exploration.ipynb`). Caso seja necessário reproduzir essa etapa, instale o extra: `pip install -e ".[notebook]"`

## Próximas etapas:

> **Status atual:** a ingestão (Bronze), o processamento intermediário e a carga para o PostgreSQL (Silver) estão implementados. A camada analítica (Gold) será desenvolvida nas próximas etapas.

* Consultas analíticas em SQL
* Documentação técnica
* Testes automatizados
* Logs e métricas do pipeline
