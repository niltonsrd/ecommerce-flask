import psycopg2
import os
from urllib.parse import urlparse


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        result = urlparse(database_url)
        return psycopg2.connect(
            database=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )

    # fallback local
    return psycopg2.connect(
        host="localhost",
        database="seu_banco",
        user="postgres",
        password="sua_senha"
    )
