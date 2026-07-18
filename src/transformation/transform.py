import json
from pathlib import Path

from src.config import settings

def transform_data(date):

    # localizar os arquivos da Bronze
    json_folder_path = Path(settings.RAW_DATA_DIR) / date

    # estruturas que representarão as tabelas do banco
    animes = []
    genres = []
    anime_genres = []
    themes = []
    anime_themes = []
    studios = []
    anime_studios = []

    # controlar IDs já processados para evitar duplicatas
    genre_ids = set()
    theme_ids = set()
    studio_ids = set()

    # percorrer todos os arquivos JSON da Bronze
    for file_path in json_folder_path.glob("*.json"):
        
        # carregar um arquivo JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        animes_data = data["data"]

        # percorrer animes
        for anime in animes_data:
            anime_id = anime["mal_id"]

            # lista de animes -> tabela anime
            animes.append(
                {
                    "mal_id": anime_id,
                    "title": anime["title"],
                    "type": anime["type"],
                    "episodes": anime["episodes"],
                    "status": anime["status"],
                    "rating": anime["rating"],
                    "score": anime["score"],
                    "scored_by": anime["scored_by"],
                    "season": anime["season"],
                    "year": anime["year"],
                }
            )

            # lista de gêneros -> tabela genre
            for genre in anime["genres"]:
                genre_id = genre["mal_id"]

                if genre_id not in genre_ids:
                    genres.append({"mal_id": genre_id, "name": genre["name"]})
                    genre_ids.add(genre_id)

                # lista de anime_genres -> tabela anime_genre
                anime_genres.append(
                    {"anime_mal_id": anime_id, "genre_mal_id": genre_id}
                )

            # lista de temas -> tabela theme
            for theme in anime["themes"]:
                theme_id = theme["mal_id"]

                if theme_id not in theme_ids:
                    themes.append({"mal_id": theme_id, "name": theme["name"]})
                    theme_ids.add(theme_id)

                # lista de anime_themes -> tabela anime_theme
                anime_themes.append(
                    {"anime_mal_id": anime_id, "theme_mal_id": theme_id}
                )

            # lista de studios -> tabela studio
            for studio in anime["studios"]:
                studio_id = studio["mal_id"]

                if studio_id not in studio_ids:
                    studios.append({"mal_id": studio_id, "name": studio["name"]})
                    studio_ids.add(studio_id)

                # lista de anime_studios -> tabela anime_studio
                anime_studios.append(
                    {"anime_mal_id": anime_id, "studio_mal_id": studio_id}
                )

    # agrupar todas as entidades transformadas
    transformed_data = {
        'animes': animes,
        'genres': genres,
        'anime_genres': anime_genres,
        'themes': themes,
        'anime_themes': anime_themes,
        'studios': studios,
        'anime_studios': anime_studios
    }

    return transformed_data
