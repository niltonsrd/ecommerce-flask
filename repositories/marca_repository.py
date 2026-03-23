from database.db import get_connection


def listar_marcas():

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, nome FROM marcas ORDER BY nome"

    cursor.execute(query)

    marcas = cursor.fetchall()

    cursor.close()
    conn.close()

    return marcas
