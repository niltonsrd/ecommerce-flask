from database.db import get_connection


def listar_modalidades_admin():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome,
        tipo,
        cidade,
        estado,
        valor,
        prazo_horas,
        prazo_dias,
        ativo
    FROM modalidades_entrega
    ORDER BY id DESC
    """

    cursor.execute(query)
    modalidades = cursor.fetchall()

    cursor.close()
    conn.close()

    return modalidades


def buscar_modalidade_por_id(modalidade_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome,
        tipo,
        cidade,
        estado,
        valor,
        prazo_horas,
        prazo_dias,
        ativo
    FROM modalidades_entrega
    WHERE id = %s
    """

    cursor.execute(query, (modalidade_id,))
    modalidade = cursor.fetchone()

    cursor.close()
    conn.close()

    return modalidade


def buscar_modalidades_checkout(cidade):
    conn = get_connection()
    cursor = conn.cursor()

    cidade_normalizada = (cidade or "").strip().lower()

    if cidade_normalizada == "salvador":
        query = """
        SELECT
            id,
            nome,
            tipo,
            cidade,
            estado,
            valor,
            prazo_horas,
            prazo_dias,
            ativo
        FROM modalidades_entrega
        WHERE ativo = TRUE
          AND tipo IN ('RETIRADA', 'LOCAL', 'MOTOBOY_CLIENTE')
          AND LOWER(COALESCE(cidade, '')) = 'salvador'
        ORDER BY valor ASC, id ASC
        """
        cursor.execute(query)
    else:
        query = """
        SELECT
            id,
            nome,
            tipo,
            cidade,
            estado,
            valor,
            prazo_horas,
            prazo_dias,
            ativo
        FROM modalidades_entrega
        WHERE ativo = TRUE
          AND tipo = 'NACIONAL'
        ORDER BY valor ASC, id ASC
        """
        cursor.execute(query)

    modalidades = cursor.fetchall()

    cursor.close()
    conn.close()

    return modalidades


def criar_modalidade(nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO modalidades_entrega (
        nome,
        tipo,
        cidade,
        estado,
        valor,
        prazo_horas,
        prazo_dias,
        ativo
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query, (nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo)
    )

    conn.commit()

    cursor.close()
    conn.close()


def atualizar_modalidade(
    modalidade_id, nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE modalidades_entrega
    SET nome = %s,
        tipo = %s,
        cidade = %s,
        estado = %s,
        valor = %s,
        prazo_horas = %s,
        prazo_dias = %s,
        ativo = %s
    WHERE id = %s
    """

    cursor.execute(
        query,
        (
            nome,
            tipo,
            cidade,
            estado,
            valor,
            prazo_horas,
            prazo_dias,
            ativo,
            modalidade_id,
        ),
    )

    conn.commit()

    cursor.close()
    conn.close()


def excluir_modalidade(modalidade_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM modalidades_entrega WHERE id = %s"

    cursor.execute(query, (modalidade_id,))

    conn.commit()

    cursor.close()
    conn.close()
