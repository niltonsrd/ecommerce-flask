from database.db import get_connection


def listar_tamanhos_repo():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, nome
    FROM tamanhos
    ORDER BY nome
    """

    cursor.execute(query)

    tamanhos = cursor.fetchall()

    cursor.close()
    conn.close()

    return tamanhos
