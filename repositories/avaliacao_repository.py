from database.db import get_connection


def criar_avaliacao(produto_id, usuario_id, nota, comentario):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO avaliacoes (produto_id, usuario_id, nota, comentario)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (produto_id, usuario_id)
    DO UPDATE SET
        nota = EXCLUDED.nota,
        comentario = EXCLUDED.comentario,
        data = CURRENT_TIMESTAMP
    """

    cursor.execute(query, (produto_id, usuario_id, nota, comentario))

    conn.commit()

    cursor.close()
    conn.close()


def listar_avaliacoes_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        a.id,
        a.nota,
        a.comentario,
        a.data,
        u.nome
    FROM avaliacoes a
    JOIN usuarios u ON u.id = a.usuario_id
    WHERE a.produto_id = %s
    ORDER BY a.data DESC
    """

    cursor.execute(query, (produto_id,))

    avaliacoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return avaliacoes


def resumo_avaliacoes_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        COALESCE(AVG(nota), 0),
        COUNT(*)
    FROM avaliacoes
    WHERE produto_id = %s
    """

    cursor.execute(query, (produto_id,))

    resumo = cursor.fetchone()

    cursor.close()
    conn.close()

    return resumo


def buscar_avaliacao_usuario(produto_id, usuario_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, nota, comentario
    FROM avaliacoes
    WHERE produto_id = %s AND usuario_id = %s
    """

    cursor.execute(query, (produto_id, usuario_id))

    avaliacao = cursor.fetchone()

    cursor.close()
    conn.close()

    return avaliacao
