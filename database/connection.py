import os
import time
import threading
from contextlib import contextmanager

import psycopg2
from psycopg2 import OperationalError, pool

from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

_connection_pool = None
_pool_lock = threading.Lock()


def _get_pool():
    global _connection_pool
    if _connection_pool is None:
        with _pool_lock:
            if _connection_pool is None:
                database_url = os.getenv("DATABASE_URL")
                min_conn = int(os.getenv("DB_POOL_MIN", 2))
                max_conn = int(os.getenv("DB_POOL_MAX", 10))

                try:
                    if database_url:
                        _connection_pool = pool.ThreadedConnectionPool(
                            min_conn, max_conn, database_url, sslmode="require"
                        )
                    else:
                        _connection_pool = pool.ThreadedConnectionPool(
                            min_conn,
                            max_conn,
                            host=DB_HOST,
                            database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD,
                        )
                except Exception as exc:
                    raise RuntimeError(
                        "Falha ao criar pool de conexões PostgreSQL. "
                        "Verifique as configurações de banco de dados."
                    ) from exc
    return _connection_pool


@contextmanager
def get_connection():
    pool_obj = _get_pool()
    conn = None
    max_retries = 3
    retry_delay = 0.1

    for attempt in range(max_retries):
        try:
            conn = pool_obj.getconn()
            if conn is not None:
                break
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise

    if conn is None:
        raise RuntimeError("Não foi possível obter conexão do pool após várias tentativas.")

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        try:
            pool_obj.putconn(conn)
        except Exception:
            pass


def init_pool():
    _get_pool()


def close_pool():
    global _connection_pool
    if _connection_pool is not None:
        _connection_pool.closeall()
        _connection_pool = None
