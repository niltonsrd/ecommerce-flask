import contextlib

from database.connection import get_connection as _get_conn_pool, init_pool, close_pool


@contextlib.contextmanager
def get_connection_cm():
    with _get_conn_pool() as conn:
        yield conn


def get_connection():
    import psycopg2
    import os
    from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

    database_url = os.getenv("DATABASE_URL")
    try:
        if database_url:
            return psycopg2.connect(database_url, sslmode="require")
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
    except Exception as exc:
        raise RuntimeError(
            "Falha ao conectar no PostgreSQL. Verifique as configurações."
        ) from exc


__all__ = ["get_connection", "get_connection_cm", "init_pool", "close_pool"]
