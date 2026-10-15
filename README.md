# Brasileirão 2024 — Análise de Dados

## Sobre o projeto

Projeto de análise de dados do Campeonato Brasileiro Série A de 2024, desenvolvido com **Python** e **SQL**.

O projeto utiliza dados de partidas para construir um pipeline ETL (Extração, Transformação e Carga), armazenar as informações em um banco de dados **SQLite** e disponibilizar estatísticas e classificações por meio de um dashboard interativo desenvolvido com **Streamlit**.

## Funcionalidades

* Extração de dados das partidas por meio da API-Football.
* Tratamento e padronização dos dados com Pandas.
* Armazenamento dos dados em um banco de dados SQLite.
* Consulta e análise dos dados utilizando SQL.
* Exibição da quantidade de partidas, total de gols e média de gols por partida.
* Ranking de clubes por gols marcados.
* Classificação final do Campeonato Brasileiro de 2024.
* Consulta da classificação de um clube específico por meio de um seletor interativo.

## Tecnologias utilizadas

* **Python:** linguagem utilizada no desenvolvimento do projeto.
* **Pandas:** tratamento e manipulação dos dados.
* **Requests:** comunicação com a API-Football.
* **python-dotenv:** gerenciamento da chave de API por meio de variáveis de ambiente.
* **SQLite:** armazenamento dos dados e consultas ao banco de dados.
* **SQL:** agregações, CTEs, junções, funções de janela e cálculos da classificação.
* **Streamlit:** construção do dashboard interativo.

## Como executar

1. **Clone o Repositório**

```Shell
git clone https://github.com/Mateus560/football-etl
cd football-etl
```

2. **Crie e ative um ambiente virtual**

```Shell
python -m venv .venv
```

No Linux:

```Shell
source .venv/bin/activate
```

3. **Instale as dependências**

```Shell
pip install -r requirements.txt
```

4. **Execute o dashboard**

```Shell
streamlit run app.py
```

## Estrutura do projeto

```
football-etl/
├── .gitignore
├── etl.ipynb
├── brasileirao.db
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

* `etl.ipynb`: notebook responsável pela extração, transformação e carga dos dados.
* `brasileirao.db`: banco de dados SQLite com as partidas do campeonato.
* `app.py`: aplicação Streamlit responsável pelo dashboard interativo.
* `requirements.txt`: dependências Python necessárias para executar o projeto.
* `.gitignore`: arquivos e pastas que não devem ser enviados ao Git.
* `LICENSE`: licença de uso do projeto.
