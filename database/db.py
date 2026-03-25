import os
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url, sslmode="require")

    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
