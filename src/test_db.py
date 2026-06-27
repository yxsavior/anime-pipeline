# print(settings.DATABASE_URL)

import psycopg2
from config import settings

conn = psycopg2.connect(settings.DATABASE_URL)

cur = conn.cursor()
cur.execute("SELECT 1;")
print(cur.fetchone())

conn.close()
