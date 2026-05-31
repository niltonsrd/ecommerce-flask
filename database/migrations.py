from pathlib import Path

from database.db import get_connection


def aplicar_migrations():
    migrations_dir = Path(__file__).resolve().parents[1] / "migrations"
    arquivos = sorted(migrations_dir.glob("*.sql"))

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute("SELECT filename FROM schema_migrations")
        aplicadas = {row[0] for row in cursor.fetchall()}

        for arquivo in arquivos:
            if arquivo.name in aplicadas:
                continue

            sql = arquivo.read_text(encoding="utf-8")
            cursor.execute(sql)
            cursor.execute(
                "INSERT INTO schema_migrations (filename) VALUES (%s)",
                (arquivo.name,),
            )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
