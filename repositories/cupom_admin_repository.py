from database.db import get_connection


def listar_cupons_admin():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        codigo,
        tipo,
        valor,
        valor_minimo,
        limite_uso,
        usos_atuais,
        ativo,
        data_inicio,
        data_fim
    FROM cupons
    ORDER BY id DESC
    """


    cursor.execute(query)
    cupons = cursor.fetchall()

    cursor.close()
    conn.close()

    return cupons


def buscar_cupom_admin(cupom_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        codigo,
        tipo,
        valor,
        valor_minimo,
        limite_uso,
        usos_atuais,
        ativo,
        data_inicio,
        data_fim
    FROM cupons
    WHERE id = %s
    """


    cursor.execute(query, (cupom_id,))
    cupom = cursor.fetchone()

    cursor.close()
    conn.close()

    return cupom


def criar_cupom_admin(
    codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO cupons (
        codigo,
        tipo,
        valor,
        valor_minimo,
        limite_uso,
        ativo,
        data_inicio,
        data_fim
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim),
    )

    conn.commit()

    cursor.close()
    conn.close()


def atualizar_cupom_admin(
    cupom_id,
    codigo,
    tipo,
    valor,
    valor_minimo,
    limite_uso,
    ativo,
    data_inicio,
    data_fim,
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE cupons
    SET codigo = %s,
        tipo = %s,
        valor = %s,
        valor_minimo = %s,
        limite_uso = %s,
        ativo = %s,
        data_inicio = %s,
        data_fim = %s
    WHERE id = %s
    """

    cursor.execute(
        query,
        (
            codigo,
            tipo,
            valor,
            valor_minimo,
            limite_uso,
            ativo,
            data_inicio,
            data_fim,
            cupom_id,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()


def excluir_cupom_admin(cupom_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM cupons WHERE id = %s"

    cursor.execute(query, (cupom_id,))

    conn.commit()

    cursor.close()
    conn.close()
