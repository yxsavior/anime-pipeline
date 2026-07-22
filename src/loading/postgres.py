import psycopg

from src.config import settings
from src.loading.prepare import prepare_processed_data

def connect():
    return psycopg.connect(settings.DATABASE_URL)

def insert_genres(conn, genres):
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO genre (mal_id, name)
            VALUES (%s, %s)
            ON CONFLICT (mal_id) DO NOTHING
            """,
            genres,
        )


def insert_themes(conn, themes):
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO theme (mal_id, name)
            VALUES (%s, %s)
            ON CONFLICT (mal_id) DO NOTHING
            """,
            themes,
        )


def insert_studios(conn, studios):
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO studio (mal_id, name)
            VALUES (%s, %s)
            ON CONFLICT (mal_id) DO NOTHING
            """,
            studios,
        )


def insert_animes(conn, animes):
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO anime (
                mal_id,
                title,
                type,
                episodes,
                status,
                rating,
                score,
                scored_by,
                season,
                year
            )
            VALUES (
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s
            )
            ON CONFLICT (mal_id) DO NOTHING
            """,
            animes,
        )


def insert_anime_genres(conn, anime_genres):
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO anime_genre (
                anime_mal_id,
                genre_mal_id
            )
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            anime_genres,
        )


def insert_anime_themes(conn, anime_themes):
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO anime_theme (
                anime_mal_id,
                theme_mal_id
            )
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            anime_themes,
        )


def insert_anime_studios(conn, anime_studios):
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO anime_studio (
                anime_mal_id,
                studio_mal_id
            )
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            anime_studios,
        )


def load_data(date):
    data = prepare_processed_data(date)

    with connect() as conn:
        insert_genres(conn, data["genres"])
        insert_themes(conn, data["themes"])
        insert_studios(conn, data["studios"])

        insert_animes(conn, data["animes"])

        insert_anime_genres(conn, data["anime_genres"])
        insert_anime_themes(conn, data["anime_themes"])
        insert_anime_studios(conn, data["anime_studios"])