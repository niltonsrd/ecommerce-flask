import argparse
import getpass
import sys
from pathlib import Path

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from scripts.import_backup_to_supabase import (
    IMPORT_ORDER,
    apply_schema_compatibility_fixes,
    existing_tables,
    reset_sequence,
    truncate_tables,
)


def connect_local():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def connect_supabase(database_url):
    return psycopg2.connect(database_url, sslmode="require")


def ordered_columns(cursor, table):
    cursor.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    )
    return [row[0] for row in cursor.fetchall()]


def fetch_rows(cursor, table, columns):
    statement = sql.SQL("SELECT {} FROM public.{} ORDER BY id").format(
        sql.SQL(", ").join(sql.Identifier(column) for column in columns),
        sql.Identifier(table),
    )
    cursor.execute(statement)
    return cursor.fetchall()


def insert_rows(cursor, table, columns, rows):
    if not rows:
        return 0

    statement = sql.SQL("INSERT INTO public.{} ({}) VALUES %s").format(
        sql.Identifier(table),
        sql.SQL(", ").join(sql.Identifier(column) for column in columns),
    )
    execute_values(cursor, statement.as_string(cursor), rows, page_size=500)
    return len(rows)


def sync_table(source_cursor, target_cursor, table):
    source_columns = set(ordered_columns(source_cursor, table))
    target_columns = ordered_columns(target_cursor, table)
    columns = [column for column in target_columns if column in source_columns]

    if not columns:
        return 0

    rows = fetch_rows(source_cursor, table, columns)
    return insert_rows(target_cursor, table, columns, rows)


def sync(database_url, dry_run=False):
    source_conn = connect_local()
    target_conn = connect_supabase(database_url)

    try:
        with source_conn:
            with target_conn:
                with source_conn.cursor() as source_cursor, target_conn.cursor() as target_cursor:
                    source_tables = existing_tables(source_cursor)
                    target_tables = existing_tables(target_cursor)
                    apply_schema_compatibility_fixes(target_cursor)

                    tables = [
                        table
                        for table in IMPORT_ORDER
                        if table in source_tables and table in target_tables
                    ]

                    if dry_run:
                        return {table: "pronto" for table in tables}

                    truncate_tables(target_cursor, tables)

                    counts = {}
                    for table in tables:
                        print(f"Sincronizando {table}...")
                        counts[table] = sync_table(source_cursor, target_cursor, table)
                        reset_sequence(target_cursor, table)

                    return counts
    finally:
        source_conn.close()
        target_conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza o PostgreSQL local atual para o Supabase."
    )
    parser.add_argument("--database-url", help="Connection string do Supabase.")
    parser.add_argument("--dry-run", action="store_true", help="Mostra tabelas sem gravar.")
    args = parser.parse_args()

    database_url = args.database_url
    if not database_url:
        database_url = getpass.getpass("Cole a DATABASE_URL do Supabase: ").strip()

    counts = sync(database_url, dry_run=args.dry_run)
    print("Sincronizacao concluida." if not args.dry_run else "Dry-run concluido.")
    for table, count in counts.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
