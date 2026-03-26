from database.db import get_connection


def obter_configuracoes():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome_loja,
        slogan,
        email_contato,
        whatsapp,
        texto_rodape,
        cor_primaria,
        cor_secundaria,
        cidade_loja,
        estado_loja,
        cor_fundo,
        cor_fundo_secundario,
        cor_texto,
        cor_texto_secundario,
        logo_url,
        mostrar_credito
    FROM configuracoes_loja
    ORDER BY id ASC
    LIMIT 1
    """

    cursor.execute(query)
    config = cursor.fetchone()

    cursor.close()
    conn.close()

    return config


def atualizar_configuracoes(
    nome_loja,
    slogan,
    email_contato,
    whatsapp,
    texto_rodape,
    cor_primaria,
    cor_secundaria,
    cidade_loja,
    estado_loja,
    cor_fundo,
    cor_fundo_secundario,
    cor_texto,
    cor_texto_secundario,
    logo_url,
    mostrar_credito,
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE configuracoes_loja
    SET nome_loja = %s,
        slogan = %s,
        email_contato = %s,
        whatsapp = %s,
        texto_rodape = %s,
        cor_primaria = %s,
        cor_secundaria = %s,
        cidade_loja = %s,
        estado_loja = %s,
        cor_fundo = %s,
        cor_fundo_secundario = %s,
        cor_texto = %s,
        cor_texto_secundario = %s,
        logo_url = %s,
        mostrar_credito = %s
    WHERE id = 1
    """

    cursor.execute(
        query,
        (
            nome_loja,
            slogan,
            email_contato,
            whatsapp,
            texto_rodape,
            cor_primaria,
            cor_secundaria,
            cidade_loja,
            estado_loja,
            cor_fundo,
            cor_fundo_secundario,
            cor_texto,
            cor_texto_secundario,
            logo_url,
            mostrar_credito,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()
