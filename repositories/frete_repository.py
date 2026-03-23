from database.db import get_connection


def buscar_frete_por_cep(cep_limpo):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome_regiao,
        cep_inicio,
        cep_fim,
        valor,
        prazo_dias,
        ativo
    FROM fretes
    WHERE ativo = TRUE
      AND %s BETWEEN cep_inicio AND cep_fim
    ORDER BY id ASC
    LIMIT 1
    """

    cursor.execute(query, (cep_limpo,))
    frete = cursor.fetchone()

    cursor.close()
    conn.close()

    return frete


def listar_fretes_admin():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome_regiao,
        cep_inicio,
        cep_fim,
        valor,
        prazo_dias,
        ativo
    FROM fretes
    ORDER BY id DESC
    """

    cursor.execute(query)
    fretes = cursor.fetchall()

    cursor.close()
    conn.close()

    return fretes


def buscar_frete_admin(frete_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome_regiao,
        cep_inicio,
        cep_fim,
        valor,
        prazo_dias,
        ativo
    FROM fretes
    WHERE id = %s
    """

    cursor.execute(query, (frete_id,))
    frete = cursor.fetchone()

    cursor.close()
    conn.close()

    return frete


def criar_frete_admin(nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO fretes (
        nome_regiao,
        cep_inicio,
        cep_fim,
        valor,
        prazo_dias,
        ativo
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo))

    conn.commit()

    cursor.close()
    conn.close()


def atualizar_frete_admin(
    frete_id, nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE fretes
    SET nome_regiao = %s,
        cep_inicio = %s,
        cep_fim = %s,
        valor = %s,
        prazo_dias = %s,
        ativo = %s
    WHERE id = %s
    """

    cursor.execute(
        query, (nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo, frete_id)
    )

    conn.commit()

    cursor.close()
    conn.close()


def excluir_frete_admin(frete_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM fretes WHERE id = %s"

    cursor.execute(query, (frete_id,))

    conn.commit()

    cursor.close()
    conn.close()
