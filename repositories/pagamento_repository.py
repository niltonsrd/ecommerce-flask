from database.db import get_connection
from datetime import datetime


def criar_pagamento(
    pedido_id, metodo, valor, status, gateway, referencia_externa=None, detalhes=None
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO pagamentos (
        pedido_id,
        metodo,
        valor,
        status,
        gateway,
        transacao_id,
        detalhes
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """

    cursor.execute(
        query,
        (
            pedido_id,
            metodo,
            valor,
            status,
            gateway,
            referencia_externa,
            detalhes,
        ),
    )

    pagamento_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return pagamento_id


def buscar_pagamento_por_pedido(pedido_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        pedido_id,
        metodo,
        status,
        valor,
        transacao_id,
        qr_code,
        codigo_pix,
        criado_em,
        atualizado_em,
        gateway,
        detalhes,
        comprovante_url,
        comprovante_enviado_em,
        observacao_cliente
    FROM pagamentos
    WHERE pedido_id = %s
    ORDER BY id DESC
    LIMIT 1
    """

    cursor.execute(query, (pedido_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "pedido_id": row[1],
        "metodo": row[2],
        "status": row[3],
        "valor": float(row[4]) if row[4] is not None else 0.0,
        "transacao_id": row[5],
        "qr_code": row[6],
        "codigo_pix": row[7],
        "criado_em": row[8],
        "atualizado_em": row[9],
        "gateway": row[10],
        "detalhes": row[11],
        "comprovante_url": row[12],
        "comprovante_enviado_em": row[13],
        "observacao_cliente": row[14],
    }


def atualizar_status_pagamento(pagamento_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE pagamentos
    SET status = %s
    WHERE id = %s
    """

    cursor.execute(query, (status, pagamento_id))

    conn.commit()
    cursor.close()
    conn.close()


def salvar_comprovante_pagamento(pedido_id, comprovante_url, observacao_cliente=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE pagamentos
    SET
        comprovante_url = %s,
        comprovante_enviado_em = NOW(),
        observacao_cliente = %s,
        status = 'EM_ANALISE',
        atualizado_em = NOW()
    WHERE pedido_id = %s
    RETURNING id
    """

    cursor.execute(query, (comprovante_url, observacao_cliente, pedido_id))
    resultado = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return resultado[0] if resultado else None
