import argparse
import getpass
import re
from pathlib import Path

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


COPY_RE = re.compile(r"^COPY public\.([a-zA-Z0-9_]+) \((.+)\) FROM stdin;$")

IMPORT_ORDER = [
    "configuracoes_loja",
    "usuarios",
    "categorias",
    "marcas",
    "tamanhos",
    "produtos",
    "produto_imagens",
    "estoque",
    "banners",
    "home_blocos",
    "fretes",
    "modalidades_entrega",
    "cupons",
    "enderecos",
    "pedidos",
    "pedido_itens",
    "pagamentos",
    "carrinho",
    "favoritos",
    "avaliacoes",
]

COLUMN_ALIASES = {
    "produtos": {
        "data_criacao": "criado_em",
    },
}


def decode_copy_value(value):
    if value == r"\N":
        return None

    escapes = {
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "v": "\v",
        "\\": "\\",
    }

    result = []
    index = 0
    while index < len(value):
        char = value[index]
        if char != "\\" or index == len(value) - 1:
            result.append(char)
            index += 1
            continue

        index += 1
        result.append(escapes.get(value[index], value[index]))
        index += 1

    return "".join(result)


def parse_backup(path):
    blocks = {}
    current_table = None
    current_columns = None
    current_rows = []

    with path.open("r", encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")

            if current_table:
                if line == r"\.":
                    blocks[current_table] = {
                        "columns": current_columns,
                        "rows": current_rows,
                    }
                    current_table = None
                    current_columns = None
                    current_rows = []
                    continue

                current_rows.append([decode_copy_value(part) for part in line.split("\t")])
                continue

            match = COPY_RE.match(line)
            if match:
                current_table = match.group(1)
                current_columns = [column.strip() for column in match.group(2).split(",")]
                current_rows = []

    return blocks


def existing_tables(cursor):
    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        """
    )
    return {row[0] for row in cursor.fetchall()}


def existing_columns(cursor, table):
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
    return {row[0] for row in cursor.fetchall()}


def truncate_tables(cursor, tables):
    if not tables:
        return

    statement = sql.SQL("TRUNCATE {} RESTART IDENTITY CASCADE").format(
        sql.SQL(", ").join(
            sql.SQL("public.{}").format(sql.Identifier(table)) for table in tables
        )
    )
    cursor.execute(statement)


def build_insert_plan(source_columns, target_columns, table):
    plan = []
    aliases = COLUMN_ALIASES.get(table, {})

    for index, source_column in enumerate(source_columns):
        target_column = aliases.get(source_column, source_column)
        if target_column in target_columns and target_column not in [item[1] for item in plan]:
            plan.append((index, target_column))

    return plan


def insert_rows(cursor, table, columns, rows):
    if not rows or not columns:
        return 0

    statement = sql.SQL("INSERT INTO public.{} ({}) VALUES %s").format(
        sql.Identifier(table),
        sql.SQL(", ").join(sql.Identifier(column) for column in columns),
    )
    execute_values(cursor, statement.as_string(cursor), rows, page_size=500)
    return len(rows)


def reset_sequence(cursor, table):
    cursor.execute("SELECT pg_get_serial_sequence(%s, 'id')", (f"public.{table}",))
    sequence = cursor.fetchone()[0]
    if not sequence:
        return

    cursor.execute(
        sql.SQL("SELECT MAX(id) FROM public.{}").format(sql.Identifier(table))
    )
    max_id = cursor.fetchone()[0]
    cursor.execute("SELECT setval(%s, %s, %s)", (sequence, max_id or 1, max_id is not None))


def apply_schema_compatibility_fixes(cursor):
    cursor.execute(
        """
        ALTER TABLE fretes
            ALTER COLUMN cep_inicio TYPE VARCHAR(20),
            ALTER COLUMN cep_fim TYPE VARCHAR(20)
        """
    )
    cursor.execute(
        """
        ALTER TABLE enderecos
            ALTER COLUMN cep TYPE VARCHAR(20)
        """
    )


def apply_post_import_fixes(cursor):
    cursor.execute(
        """
        UPDATE configuracoes_loja
        SET background_url = COALESCE(NULLIF(background_url, ''), 'background.jpg')
        WHERE id = (SELECT MIN(id) FROM configuracoes_loja)
        """
    )


def import_backup(database_url, backup_path):
    blocks = parse_backup(backup_path)

    conn = psycopg2.connect(database_url, sslmode="require")
    try:
        with conn:
            with conn.cursor() as cursor:
                target_tables = existing_tables(cursor)
                apply_schema_compatibility_fixes(cursor)
                import_tables = [table for table in IMPORT_ORDER if table in blocks and table in target_tables]
                import_tables.extend(
                    table
                    for table in blocks
                    if table not in import_tables and table in target_tables
                )

                truncate_tables(cursor, import_tables)

                imported_counts = {}
                for table in import_tables:
                    print(f"Importando {table}...")
                    target_columns = existing_columns(cursor, table)
                    source_columns = blocks[table]["columns"]
                    plan = build_insert_plan(source_columns, target_columns, table)

                    insert_columns = [target_column for _, target_column in plan]
                    insert_data = [
                        [row[source_index] for source_index, _ in plan]
                        for row in blocks[table]["rows"]
                    ]

                    imported_counts[table] = insert_rows(
                        cursor, table, insert_columns, insert_data
                    )
                    reset_sequence(cursor, table)

                apply_post_import_fixes(cursor)

        return imported_counts
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Importa o backup.sql antigo para o PostgreSQL do Supabase."
    )
    parser.add_argument("--database-url", help="Connection string do Supabase.")
    parser.add_argument("--backup", default="backup.sql", help="Arquivo SQL de backup.")
    args = parser.parse_args()

    database_url = args.database_url
    if not database_url:
        database_url = getpass.getpass("Cole a DATABASE_URL do Supabase: ").strip()

    backup_path = Path(args.backup).resolve()
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup nao encontrado: {backup_path}")

    counts = import_backup(database_url, backup_path)
    print("Importacao concluida.")
    for table, count in counts.items():
        print(f"{table}: {count}")


if __name__ == "__main__":
    main()
