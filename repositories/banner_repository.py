from database.db import get_connection


def listar_banners_admin():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        titulo,
        subtitulo,
        imagem_url,
        link,
        ativo,
        ordem
    FROM banners
    ORDER BY ordem ASC, id ASC
    """

    cursor.execute(query)
    banners = cursor.fetchall()

    cursor.close()
    conn.close()

    return banners


def listar_banners_ativos():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        titulo,
        subtitulo,
        imagem_url,
        link,
        ativo,
        ordem
    FROM banners
    WHERE ativo = TRUE
    ORDER BY ordem ASC, id ASC
    """

    cursor.execute(query)
    banners = cursor.fetchall()

    cursor.close()
    conn.close()

    return banners


def buscar_banner_por_id(banner_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        titulo,
        subtitulo,
        imagem_url,
        link,
        ativo,
        ordem
    FROM banners
    WHERE id = %s
    """

    cursor.execute(query, (banner_id,))
    banner = cursor.fetchone()

    cursor.close()
    conn.close()

    return banner


def criar_banner(titulo, subtitulo, imagem_url, link, ativo, ordem):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO banners (
        titulo,
        subtitulo,
        imagem_url,
        link,
        ativo,
        ordem
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (titulo, subtitulo, imagem_url, link, ativo, ordem))

    conn.commit()

    cursor.close()
    conn.close()


def atualizar_banner(banner_id, titulo, subtitulo, imagem_url, link, ativo, ordem):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE banners
    SET titulo = %s,
        subtitulo = %s,
        imagem_url = %s,
        link = %s,
        ativo = %s,
        ordem = %s
    WHERE id = %s
    """

    cursor.execute(
        query, (titulo, subtitulo, imagem_url, link, ativo, ordem, banner_id)
    )

    conn.commit()

    cursor.close()
    conn.close()


def excluir_banner(banner_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM banners WHERE id = %s"

    cursor.execute(query, (banner_id,))

    conn.commit()

    cursor.close()
    conn.close()
