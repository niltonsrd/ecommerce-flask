from database.db import get_connection
from datetime import datetime


def buscar_cupom_por_codigo(codigo):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        codigo,
        tipo,
        valor,
        ativo,
        data_inicio,
        data_fim,
        valor_minimo,
        limite_uso,
        usos_atuais
    FROM cupons
    WHERE codigo = %s
    """

    cursor.execute(query, (codigo,))

    cupom = cursor.fetchone()

    cursor.close()
    conn.close()

    return cupom


def incrementar_uso_cupom(cupom_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE cupons
    SET usos_atuais = COALESCE(usos_atuais, 0) + 1
    WHERE id = %s
    """

    cursor.execute(query, (cupom_id,))

    conn.commit()

    cursor.close()
    conn.close()
