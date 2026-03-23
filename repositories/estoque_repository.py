from database.db import get_connection


def listar_tamanhos():

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, nome FROM tamanhos ORDER BY nome"

    cursor.execute(query)

    tamanhos = cursor.fetchall()

    cursor.close()
    conn.close()

    return tamanhos


def salvar_estoque(produto_id, tamanho_id, quantidade):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO estoque (produto_id, tamanho_id, quantidade)
    VALUES (%s, %s, %s)
    ON CONFLICT (produto_id, tamanho_id)
    DO UPDATE SET quantidade = estoque.quantidade + EXCLUDED.quantidade;
    """

    cursor.execute(query, (produto_id, tamanho_id, quantidade))

    conn.commit()

    cursor.close()
    conn.close()


def verificar_estoque(produto_id, tamanho_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT quantidade
    FROM estoque
    WHERE produto_id = %s
    AND tamanho_id = %s
    """

    cursor.execute(query, (produto_id, tamanho_id))

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado


def reduzir_estoque(produto_id, tamanho_id, quantidade):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE estoque
    SET quantidade = quantidade - %s
    WHERE produto_id = %s
    AND tamanho_id = %s
    """

    cursor.execute(query, (quantidade, produto_id, tamanho_id))

    conn.commit()

    cursor.close()
    conn.close()
