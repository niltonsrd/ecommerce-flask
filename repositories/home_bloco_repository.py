from database.db import get_connection


def listar_blocos_home():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome,
        tipo_bloco,
        layout,
        titulo,
        subtitulo,
        descricao,
        imagem_url,
        texto_botao,
        link_botao,
        texto_botao_secundario,
        link_botao_secundario,
        cor_fundo,
        cor_texto,
        alinhamento_texto,
        ordem,
        ativo,
        criado_em
    FROM home_blocos
    ORDER BY ordem ASC, id ASC
    """

    cursor.execute(query)
    blocos = cursor.fetchall()

    cursor.close()
    conn.close()

    return blocos


def listar_blocos_home_ativos():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome,
        tipo_bloco,
        layout,
        titulo,
        subtitulo,
        descricao,
        imagem_url,
        texto_botao,
        link_botao,
        texto_botao_secundario,
        link_botao_secundario,
        cor_fundo,
        cor_texto,
        alinhamento_texto,
        ordem,
        ativo,
        criado_em
    FROM home_blocos
    WHERE ativo = TRUE
    ORDER BY ordem ASC, id ASC
    """

    cursor.execute(query)
    blocos = cursor.fetchall()

    cursor.close()
    conn.close()

    return blocos


def obter_bloco_home_por_id(bloco_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome,
        tipo_bloco,
        layout,
        titulo,
        subtitulo,
        descricao,
        imagem_url,
        texto_botao,
        link_botao,
        texto_botao_secundario,
        link_botao_secundario,
        cor_fundo,
        cor_texto,
        alinhamento_texto,
        ordem,
        ativo,
        criado_em
    FROM home_blocos
    WHERE id = %s
    """

    cursor.execute(query, (bloco_id,))
    bloco = cursor.fetchone()

    cursor.close()
    conn.close()

    return bloco


def criar_bloco_home(
    nome,
    tipo_bloco,
    layout,
    titulo,
    subtitulo,
    descricao,
    imagem_url,
    texto_botao,
    link_botao,
    texto_botao_secundario,
    link_botao_secundario,
    cor_fundo,
    cor_texto,
    alinhamento_texto,
    ordem,
    ativo,
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO home_blocos (
        nome,
        tipo_bloco,
        layout,
        titulo,
        subtitulo,
        descricao,
        imagem_url,
        texto_botao,
        link_botao,
        texto_botao_secundario,
        link_botao_secundario,
        cor_fundo,
        cor_texto,
        alinhamento_texto,
        ordem,
        ativo
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            nome,
            tipo_bloco,
            layout,
            titulo,
            subtitulo,
            descricao,
            imagem_url,
            texto_botao,
            link_botao,
            texto_botao_secundario,
            link_botao_secundario,
            cor_fundo,
            cor_texto,
            alinhamento_texto,
            ordem,
            ativo,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()


def editar_bloco_home(
    bloco_id,
    nome,
    tipo_bloco,
    layout,
    titulo,
    subtitulo,
    descricao,
    imagem_url,
    texto_botao,
    link_botao,
    texto_botao_secundario,
    link_botao_secundario,
    cor_fundo,
    cor_texto,
    alinhamento_texto,
    ordem,
    ativo,
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE home_blocos
    SET nome = %s,
        tipo_bloco = %s,
        layout = %s,
        titulo = %s,
        subtitulo = %s,
        descricao = %s,
        imagem_url = %s,
        texto_botao = %s,
        link_botao = %s,
        texto_botao_secundario = %s,
        link_botao_secundario = %s,
        cor_fundo = %s,
        cor_texto = %s,
        alinhamento_texto = %s,
        ordem = %s,
        ativo = %s
    WHERE id = %s
    """

    cursor.execute(
        query,
        (
            nome,
            tipo_bloco,
            layout,
            titulo,
            subtitulo,
            descricao,
            imagem_url,
            texto_botao,
            link_botao,
            texto_botao_secundario,
            link_botao_secundario,
            cor_fundo,
            cor_texto,
            alinhamento_texto,
            ordem,
            ativo,
            bloco_id,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()


def excluir_bloco_home(bloco_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM home_blocos WHERE id = %s"
    cursor.execute(query, (bloco_id,))

    conn.commit()

    cursor.close()
    conn.close()
