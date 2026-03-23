from database.db import get_connection


def adicionar_favorito(usuario_id, produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO favoritos (usuario_id, produto_id)
    VALUES (%s, %s)
    """

    cursor.execute(query, (usuario_id, produto_id))

    conn.commit()

    cursor.close()
    conn.close()


def listar_favoritos(usuario_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        f.id,
        p.id,
        p.nome,
        p.preco
    FROM favoritos f
    JOIN produtos p ON p.id = f.produto_id
    WHERE f.usuario_id = %s
    ORDER BY f.id DESC
    """

    cursor.execute(query, (usuario_id,))

    favoritos = cursor.fetchall()

    cursor.close()
    conn.close()

    return favoritos


def remover_favorito(favorito_id, usuario_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    DELETE FROM favoritos
    WHERE id = %s AND usuario_id = %s
    """

    cursor.execute(query, (favorito_id, usuario_id))

    conn.commit()

    cursor.close()
    conn.close()


def verificar_favorito(usuario_id, produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id
    FROM favoritos
    WHERE usuario_id = %s AND produto_id = %s
    """

    cursor.execute(query, (usuario_id, produto_id))

    favorito = cursor.fetchone()

    cursor.close()
    conn.close()

    return favorito
