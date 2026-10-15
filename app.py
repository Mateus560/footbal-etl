import streamlit as st, sqlite3
import pandas as pd

connection = sqlite3.connect("brasileirao.db")
query = pd.read_sql("""
    SELECT 
        data AS Data,
        rodada AS Rodada,
        mandante AS Mandante,
        visitante AS Visitante,
        gols_mandante AS 'Gols do Mandante', 
        gols_visitante AS 'Gols do Visitante'
    FROM partidas LIMIT 5;
""", connection
)

clubes = pd.read_sql("""
    SELECT mandante AS clube FROM partidas
    UNION
    SELECT visitante AS clube FROM partidas
    ORDER BY clube;
""", connection)

print(clubes.to_string(index=False))

query["Data"] = pd.to_datetime(query["Data"]).dt.strftime("%d/%m/%Y")

query_resumo = pd.read_sql("""
    SELECT 
        COUNT(*) AS 'Quantidade de Partidas',
        SUM(gols_mandante) + SUM(gols_visitante) AS 'Total de Gols',
        (SUM(gols_mandante) + SUM(gols_visitante)) / (COUNT(*) * 1.0) AS 'Média de Gols por Partida'
    FROM partidas;
""", connection
)

st.title("Brasileirão 2024")
col1, col2, col3 = st.columns(3)
col1.metric(
    "Quantidade de Partidas",
    query_resumo.loc[0, "Quantidade de Partidas"]
)

col2.metric(
    "Total de Gols",
    query_resumo.loc[0, "Total de Gols"]
)

col3.metric(
    "Média de Gols por Partida",
    f"{query_resumo.loc[0, 'Média de Gols por Partida']:.2f}".replace(".", ",")
)
st.dataframe(query, hide_index=True)

query_ranking = pd.read_sql("""
    WITH gols_mandante AS (
        SELECT  
            mandante,
            SUM(gols_mandante) AS total_gols_mandante
        FROM partidas
        GROUP BY mandante
    ),
    
    gols_visitante AS (
        SELECT
            visitante,
            SUM(gols_visitante) AS total_gols_visitante
        FROM partidas
        GROUP BY visitante
    ),

    gols_clube AS (
        SELECT 
            m.mandante AS clube,
            m.total_gols_mandante + v.total_gols_visitante AS total_gols,
            ROW_NUMBER () OVER(ORDER BY m.total_gols_mandante + v.total_gols_visitante DESC) AS pos
        FROM gols_mandante m
        INNER JOIN gols_visitante v
            ON m.mandante = v.visitante
    )
    
    SELECT
        pos AS 'Posição',
        clube AS Clube,
        total_gols AS 'Total de Gols'
    FROM gols_clube
    ORDER BY pos;
""", connection
)
ranking = query_ranking

st.subheader("Ranking de Gols por Clube")
st.bar_chart(ranking, x="Clube", y="Total de Gols")

query_classificacao = pd.read_sql("""
    SELECT 
        ROW_NUMBER() OVER(ORDER BY SUM(Pontos) DESC, SUM(Gols_Marcados) - SUM(Gols_Sofridos) DESC, Gols_Marcados DESC) AS 'Posição',
        Clube,
        SUM(Pontos) AS Pts,
        SUM(Vitorias) AS VIT,
        SUM(Empates) AS E,
        SUM(Derrotas) AS DER,
        SUM(Gols_Marcados) AS GM,
        SUM(Gols_Sofridos) AS GC,
        SUM(Gols_Marcados) - SUM(Gols_Sofridos) AS SG
    FROM (
        SELECT
            mandante AS Clube,
            SUM(CASE
                WHEN gols_mandante > gols_visitante THEN 3
                WHEN gols_mandante < gols_visitante THEN 0
                ELSE 1
            END) AS Pontos,
            SUM(CASE
                WHEN gols_mandante > gols_visitante THEN 1
                ELSE 0
            END) AS Vitorias,
            SUM(CASE
                WHEN gols_mandante < gols_visitante THEN 1
                ELSE 0
            END) AS Derrotas,
            SUM(CASE
                WHEN gols_mandante = gols_visitante THEN 1
                ELSE 0
            END) AS Empates,
            SUM(gols_mandante) AS Gols_Marcados,
            SUM(gols_visitante) AS Gols_Sofridos,
            SUM(gols_mandante) - SUM(gols_visitante) AS Saldo_de_Gol
        FROM partidas
        GROUP BY Clube
        
        UNION ALL
            
        SELECT
            visitante AS Clube,
            SUM(CASE
                WHEN gols_visitante > gols_mandante THEN 3
                WHEN gols_visitante < gols_mandante THEN 0
                ELSE 1
            END) AS Pontos,
            SUM(CASE
                WHEN gols_visitante > gols_mandante THEN 1
                ELSE 0
            END) AS Vitorias,
            SUM(CASE
                WHEN gols_visitante < gols_mandante THEN 1
                ELSE 0
            END) AS Derrotas,
            SUM(CASE
                WHEN gols_visitante = gols_mandante THEN 1
                ELSE 0
            END) AS Empates,
            SUM(gols_visitante) AS Gols_Marcados,
            SUM(gols_mandante) AS Gols_Sofridos,
            SUM(gols_visitante) - SUM(gols_mandante) AS Saldo_de_Gol
        FROM partidas
        GROUP BY Clube
    )
    GROUP BY Clube
    ORDER BY Posição;
""", connection
)

classificacao = query_classificacao
clubes = classificacao["Clube"].tolist()
clube_selecionado = st.selectbox("Escolha um clube", clubes)
dados_clube = classificacao[
    classificacao["Clube"] == clube_selecionado
]
st.dataframe(dados_clube, hide_index=True)
st.subheader("Classificação Geral")
st.dataframe(classificacao, hide_index=True)