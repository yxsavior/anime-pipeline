from src.config import settings
import psycopg

# abrir uma conexão usando with e settings.DATABASE_URL;
# abrir um cursor;
# executar: SELECT 1;
# ler o resultado;

def test_connection():
    with psycopg.connect(settings.DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

            if result == (1,):
                print("Database connection successful.")
            else:
                print("Unexpected database response:", result)

final_test = test_connection()