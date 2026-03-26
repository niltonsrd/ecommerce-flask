from database.db import get_connection


def normalizar_status_dashboard(status):
    status = (status or "").strip().lower()

    mapa = {
        "pendente": "pendente",
        "aguardando pagamento": "pendente",
        "pago": "pago",
        "aprovado": "pago",
        "em separacao": "em_separacao",
        "em separação": "em_separacao",
        "separando": "em_separacao",
        "enviado": "enviado",
        "postado": "enviado",
        "entregue": "entregue",
        "finalizado": "entregue",
        "cancelado": "cancelado",
        "cancelada": "cancelado",
    }

    return mapa.get(status, "pendente")


def buscar_faturamento_total():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(valor_total), 0)
        FROM pedidos
        WHERE LOWER(COALESCE(status, 'pendente')) NOT IN ('cancelado', 'cancelada')
    """
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return float(resultado or 0)


def buscar_faturamento_hoje():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(valor_total), 0)
        FROM pedidos
        WHERE DATE(data_pedido) = CURRENT_DATE
          AND LOWER(COALESCE(status, 'pendente')) NOT IN ('cancelado', 'cancelada')
    """
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return float(resultado or 0)


def buscar_faturamento_mes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(valor_total), 0)
        FROM pedidos
        WHERE DATE_TRUNC('month', data_pedido) = DATE_TRUNC('month', CURRENT_DATE)
          AND LOWER(COALESCE(status, 'pendente')) NOT IN ('cancelado', 'cancelada')
    """
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return float(resultado or 0)


def buscar_pedidos_hoje():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM pedidos
        WHERE DATE(data_pedido) = CURRENT_DATE
    """
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return int(resultado or 0)


def buscar_pedidos_pendentes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM pedidos
        WHERE LOWER(COALESCE(status, 'pendente')) IN (
            'pendente',
            'aguardando pagamento',
            'pago',
            'em separacao',
            'em separação',
            'separando'
        )
    """
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return int(resultado or 0)


def buscar_clientes_novos_hoje():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM usuarios
        WHERE DATE(data_criacao) = CURRENT_DATE
          AND (
                LOWER(COALESCE(tipo_usuario, '')) = 'cliente'
                OR LOWER(COALESCE(tipo, '')) = 'cliente'
              )
    """
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return int(resultado or 0)


def buscar_ticket_medio():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(AVG(valor_total), 0)
        FROM pedidos
        WHERE LOWER(COALESCE(status, 'pendente')) NOT IN ('cancelado', 'cancelada')
    """
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return float(resultado or 0)


def buscar_total_estoque_critico(quantidade_minima=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM estoque e
        INNER JOIN produtos p ON p.id = e.produto_id
        WHERE e.quantidade <= %s
          AND p.ativo = TRUE
    """,
        (quantidade_minima,),
    )

    resultado = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return int(resultado or 0)


def buscar_produtos_mais_vendidos(limite=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            p.id,
            p.nome,
            COALESCE(SUM(pi.quantidade), 0) AS total_vendido
        FROM pedido_itens pi
        INNER JOIN produtos p ON p.id = pi.produto_id
        INNER JOIN pedidos ped ON ped.id = pi.pedido_id
        WHERE LOWER(COALESCE(ped.status, 'pendente')) NOT IN ('cancelado', 'cancelada')
        GROUP BY p.id, p.nome
        ORDER BY total_vendido DESC, p.nome ASC
        LIMIT %s
    """,
        (limite,),
    )

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": item[0],
            "nome": item[1],
            "total_vendido": int(item[2] or 0),
        }
        for item in resultados
    ]


def buscar_estoque_baixo(limite=10, quantidade_minima=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            p.id,
            p.nome,
            t.nome,
            e.quantidade
        FROM estoque e
        INNER JOIN produtos p ON p.id = e.produto_id
        INNER JOIN tamanhos t ON t.id = e.tamanho_id
        WHERE e.quantidade <= %s
          AND p.ativo = TRUE
        ORDER BY e.quantidade ASC, p.nome ASC
        LIMIT %s
    """,
        (quantidade_minima, limite),
    )

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": item[0],
            "nome": item[1],
            "tamanho": item[2],
            "quantidade": int(item[3] or 0),
        }
        for item in resultados
    ]


def buscar_status_pedidos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT LOWER(COALESCE(status, 'pendente')) AS status, COUNT(*)
        FROM pedidos
        GROUP BY LOWER(COALESCE(status, 'pendente'))
    """
    )

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    base = {
        "pendente": 0,
        "pago": 0,
        "em_separacao": 0,
        "enviado": 0,
        "entregue": 0,
        "cancelado": 0,
    }

    for status, total in resultados:
        chave = normalizar_status_dashboard(status)
        if chave in base:
            base[chave] += int(total or 0)

    return base


def buscar_expedicao():
    status = buscar_status_pedidos()

    return {
        "aguardando_pagamento": status["pendente"],
        "pagos": status["pago"],
        "em_separacao": status["em_separacao"],
        "enviados": status["enviado"],
        "entregues": status["entregue"],
    }


def buscar_pedidos_recentes(limite=8):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            ped.id,
            COALESCE(u.nome, 'Cliente sem nome') AS cliente_nome,
            COALESCE(u.email, '') AS cliente_email,
            COALESCE(u.telefone, '') AS cliente_telefone,
            COALESCE(ped.valor_total, 0) AS valor_total,
            COALESCE(ped.status, 'PENDENTE') AS status,
            ped.data_pedido,
            COALESCE(STRING_AGG(DISTINCT pr.nome, ', '), 'Sem itens') AS itens_resumo,
            COALESCE(ped.valor_frete, 0) AS valor_frete,
            COALESCE(ped.forma_pagamento, '') AS forma_pagamento
        FROM pedidos ped
        LEFT JOIN usuarios u ON u.id = ped.usuario_id
        LEFT JOIN pedido_itens pi ON pi.pedido_id = ped.id
        LEFT JOIN produtos pr ON pr.id = pi.produto_id
        GROUP BY
            ped.id,
            u.nome,
            u.email,
            u.telefone,
            ped.valor_total,
            ped.status,
            ped.data_pedido,
            ped.valor_frete,
            ped.forma_pagamento
        ORDER BY ped.data_pedido DESC
        LIMIT %s
    """,
        (limite,),
    )

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": item[0],
            "cliente_nome": item[1],
            "cliente_email": item[2],
            "cliente_telefone": item[3],
            "total": float(item[4] or 0),
            "status": item[5],
            "data_pedido": item[6],
            "itens_resumo": item[7],
            "valor_frete": float(item[8] or 0),
            "forma_pagamento": item[9],
        }
        for item in resultados
    ]


def buscar_clientes_recentes(limite=6):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            COALESCE(nome, 'Cliente') AS nome,
            COALESCE(email, '') AS email,
            COALESCE(telefone, '') AS telefone,
            data_criacao
        FROM usuarios
        WHERE (
                LOWER(COALESCE(tipo_usuario, '')) = 'cliente'
                OR LOWER(COALESCE(tipo, '')) = 'cliente'
              )
        ORDER BY data_criacao DESC
        LIMIT %s
    """,
        (limite,),
    )

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": item[0],
            "nome": item[1],
            "email": item[2],
            "telefone": item[3],
            "data_criacao": item[4],
        }
        for item in resultados
    ]
