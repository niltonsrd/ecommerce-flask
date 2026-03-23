from database.db import get_connection


def listar_categorias():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, nome, imagem_url
    FROM categorias
    ORDER BY nome
    """

    cursor.execute(query)
    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    return categorias


def buscar_categoria_por_id(categoria_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, nome, imagem_url
    FROM categorias
    WHERE id = %s
    """

    cursor.execute(query, (categoria_id,))
    categoria = cursor.fetchone()

    cursor.close()
    conn.close()

    return categoria


def criar_categoria(nome, imagem_url=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO categorias (nome, imagem_url)
    VALUES (%s, %s)
    """

    cursor.execute(query, (nome, imagem_url))
    conn.commit()

    cursor.close()
    conn.close()


def atualizar_categoria(categoria_id, nome, imagem_url=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE categorias
    SET nome = %s, imagem_url = %s
    WHERE id = %s
    """

    cursor.execute(query, (nome, imagem_url, categoria_id))
    conn.commit()

    cursor.close()
    conn.close()
