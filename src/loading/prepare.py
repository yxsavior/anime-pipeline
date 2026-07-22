from pathlib import Path
import json

from src.config import settings

def read_json(filename, date):
    folder = Path(settings.PROCESSED_DATA_DIR) / date

    with open(folder / f"{filename}.json", encoding="utf-8") as f:
        return json.load(f)

# transformar uma lista de dicionários em uma lista de tuplas
# genre, theme, studio
def prepare_lookup(records):
    return [
        (record["mal_id"], record["name"])
        for record in records
    ]

def prepare_anime(animes):
    return [
        (
            anime["mal_id"],
            anime["title"],
            anime["type"],
            anime["episodes"],
            anime["status"],
            anime["rating"],
            anime["score"],
            anime["scored_by"],
            anime["season"],
            anime["year"],
        )
        for anime in animes
    ]

def prepare_relationship(records, left_key, right_key):
    return [
        (record[left_key], record[right_key])
        for record in records
    ]

# lê os JSONs (dicionários) processados e adapta os registros
# para o formato esperado pelo executemany() que é uma lista de tuplas
def prepare_processed_data(date):
    return {
        "genres": prepare_lookup(read_json("genres", date)),
        "themes": prepare_lookup(read_json("themes", date)),
        "studios": prepare_lookup(read_json("studios", date)),
        "animes": prepare_anime(read_json("animes", date)),
        "anime_genres": prepare_relationship(
            read_json("anime_genres", date),
            "anime_mal_id",
            "genre_mal_id",
        ),
        "anime_themes": prepare_relationship(
            read_json("anime_themes", date),
            "anime_mal_id",
            "theme_mal_id",
        ),
        "anime_studios": prepare_relationship(
            read_json("anime_studios", date),
            "anime_mal_id",
            "studio_mal_id",
        ),
    }
