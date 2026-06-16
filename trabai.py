import pandas as pd

df_movies = pd.read_csv('/content/tmdb_5000_movies.csv')
df_movies.head(5)

df_credits = pd.read_csv('/content/tmdb_5000_credits.csv')
df_credits.head(5)

import json
import ast

def converter_json(coluna_texto):
    if pd.isna(coluna_texto):
        return []
    try:
        return json.loads(coluna_texto)
    except json.JSONDecodeError:
        return ast.literal_eval(coluna_texto)

df_movies["genres"] = df_movies["genres"].apply(converter_json)
df_movies["keywords"] = df_movies["keywords"].apply(converter_json)
df_credits["cast"] = df_credits["cast"].apply(converter_json)
df_credits["crew"] = df_credits["crew"].apply(converter_json)

df_movies.head(5)

df_genres_exploded = df_movies[["id", "genres"]].explode("genres")

df_genres_exploded = df_genres_exploded.dropna(subset=["genres"])

df_genres_normalized = pd.json_normalize(df_genres_exploded["genres"])
df_genres_normalized.index = df_genres_exploded.index

df_genres_normalized_renamed = df_genres_normalized.rename(columns={"id": "id_genero"})

df_filme_genero_bruto = pd.concat(
    [df_genres_exploded[["id"]], df_genres_normalized_renamed], axis=1
)
df_filme_genero_bruto.rename(columns={"id": "id_filme"}, inplace=True)

tb_genero = (
    df_filme_genero_bruto[["id_genero", "name"]]
    .drop_duplicates()
    .rename(columns={"id_genero": "id_genero", "name": "nome_genero"})
)

tb_filme_genero = df_filme_genero_bruto[["id_filme", "id_genero"]].rename(
    columns={"id_genero": "id_genero"}
)

df_cast_exploded = df_credits[["movie_id", "cast"]].explode("cast").dropna()

df_cast_normalized = pd.json_normalize(df_cast_exploded["cast"])
df_cast_normalized.index = df_cast_exploded.index

df_cast_final = pd.concat(
    [df_cast_exploded[["movie_id"]], df_cast_normalized], axis=1
)

tb_ator = (
    df_cast_final[["id", "name"]]
    .drop_duplicates()
    .rename(columns={"id": "id_ator", "name": "nome_ator"})
)

tb_filme_ator = df_cast_final[["movie_id", "id", "character"]].rename(
    columns={"movie_id": "id_filme", "id": "id_ator", "character": "papel"}
)

df_crew_exploded = df_credits[["movie_id", "crew"]].explode("crew").dropna()

df_crew_normalized = pd.json_normalize(df_crew_exploded["crew"])
df_crew_normalized.index = df_crew_exploded.index

df_crew_final = pd.concat(
    [df_crew_exploded[["movie_id"]], df_crew_normalized], axis=1
)

df_diretores = df_crew_final[df_crew_final["job"] == "Director"]

tb_diretor = (
    df_diretores[["id", "name"]]
    .drop_duplicates()
    .rename(columns={"id": "id_diretor", "name": "nome_diretor"})
)

df_mapeamento_diretor = df_diretores[["movie_id", "id"]].rename(
    columns={"movie_id": "id_filme", "id": "id_diretor"}
)

tb_filme = df_movies[
    [
        "id",
        "title",
        "release_date",
        "budget",
        "revenue",
        "vote_average",
        "vote_count",
        "popularity",
    ]
].rename(columns={"id": "id_filme", "release_date": "data_lanc"})

tb_filme = pd.merge(
    tb_filme, df_mapeamento_diretor, on="id_filme", how="left"
)

tb_filme = tb_filme.drop_duplicates(subset=["id_filme"])

import os

diretorio_saida = "dados_normalizados"
if not os.path.exists(diretorio_saida):
    os.makedirs(diretorio_saida)


config_exportacao = {
    "sep": ";",
    "index": False,
    "encoding": "utf-8",
}

tb_diretor.to_csv(
    os.path.join(diretorio_saida, "tb_diretor.csv"), **config_exportacao
)
tb_ator.to_csv(
    os.path.join(diretorio_saida, "tb_ator.csv"), **config_exportacao
)
tb_genero.to_csv(
    os.path.join(diretorio_saida, "tb_genero.csv"), **config_exportacao
)

tb_filme.to_csv(
    os.path.join(diretorio_saida, "tb_filme.csv"), **config_exportacao
)

tb_filme_genero.to_csv(
    os.path.join(diretorio_saida, "tb_filme_genero.csv"), **config_exportacao
)
tb_filme_ator.to_csv(
    os.path.join(diretorio_saida, "tb_filme_ator.csv"), **config_exportacao
)

df_filmes = pd.read_csv("dados_normalizados/tb_filme.csv", sep=";")
df_filmes["data_lanc"] = pd.to_datetime(df_filmes["data_lanc"], errors="coerce")

data_min = df_filmes["data_lanc"].min()
data_max = df_filmes["data_lanc"].max()

if pd.isna(data_min) or pd.isna(data_max):
    data_min = pd.to_datetime("1900-01-01")
    data_max = pd.to_datetime("2026-12-31")

sequencia_datas = pd.date_range(start=data_min, end=data_max, freq="D")

d_calendario = pd.DataFrame({"data": sequencia_datas})

d_calendario["ano"] = d_calendario["data"].dt.year
d_calendario["mes"] = d_calendario["data"].dt.month
d_calendario["nome_mes"] = d_calendario["data"].dt.strftime("%B")
d_calendario["trimestre"] = d_calendario["data"].dt.quarter
d_calendario["dia_semana"] = d_calendario["data"].dt.dayofweek
d_calendario["ano_mes"] = d_calendario["data"].dt.strftime("%Y-%m")

d_calendario.to_csv("d_calendario.csv", sep=";", index=False, encoding="utf-8")