from database.db import get_connection


def listar_pedidos():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        p.id,
        u.nome,
        p.valor_total,
        p.status,
        COALESCE(p.criado_em, p.data_pedido) AS data_pedido
    FROM pedidos p
    JOIN usuarios u ON u.id = p.usuario_id
    ORDER BY p.id DESC
    """

    cursor.execute(query)
    pedidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return pedidos


def atualizar_status(pedido_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE pedidos
    SET status = %s
    WHERE id = %s
    """

    cursor.execute(query, (status, pedido_id))
    conn.commit()

    cursor.close()
    conn.close()


def buscar_status_pedido(pedido_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT status
    FROM pedidos
    WHERE id = %s
    LIMIT 1
    """

    cursor.execute(query, (pedido_id,))
    status = cursor.fetchone()

    cursor.close()
    conn.close()

    return status


def buscar_itens_admin_pedido(pedido_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        produto_id,
        tamanho_id,
        quantidade
    FROM pedido_itens
    WHERE pedido_id = %s
    ORDER BY id ASC
    """

    cursor.execute(query, (pedido_id,))
    itens = cursor.fetchall()

    cursor.close()
    conn.close()

    return itens


def listar_pedidos_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        valor_total,
        status,
        COALESCE(criado_em, data_pedido) AS data_pedido
    FROM pedidos
    WHERE usuario_id = %s
    ORDER BY id DESC
    """

    cursor.execute(query, (usuario_id,))
    pedidos = cursor.fetchall()

    cursor.close()
    conn.close()

    return pedidos


def buscar_itens_pedido(pedido_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        p.id,
        p.status,
        p.valor_total,
        COALESCE(p.criado_em, p.data_pedido) AS data_pedido,
        pr.nome,
        pi.quantidade,
        pi.preco,
        t.nome AS tamanho_nome,
        p.subtotal,
        p.desconto,
        p.valor_frete,
        p.forma_pagamento,
        p.prazo_entrega,
        p.observacoes
    FROM pedidos p
    JOIN pedido_itens pi ON pi.pedido_id = p.id
    JOIN produtos pr ON pr.id = pi.produto_id
    LEFT JOIN tamanhos t ON t.id = pi.tamanho_id
    WHERE p.id = %s
      AND p.usuario_id = %s
    ORDER BY pi.id ASC
    """

    cursor.execute(query, (pedido_id, usuario_id))
    itens = cursor.fetchall()

    cursor.close()
    conn.close()

    return itens
