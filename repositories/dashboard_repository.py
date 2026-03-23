from database.db import get_connection


def buscar_faturamento_total():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(valor_total), 0)
        FROM pedidos
        WHERE status NOT IN ('cancelado', 'cancelada')
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
          AND status NOT IN ('cancelado', 'cancelada')
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


def buscar_clientes_novos_hoje():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM usuarios
        WHERE tipo_usuario = 'cliente'
          AND DATE(data_criacao) = CURRENT_DATE
    """
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
        WHERE ped.status NOT IN ('cancelado', 'cancelada')
        GROUP BY p.id, p.nome
        ORDER BY total_vendido DESC, p.nome ASC
        LIMIT %s
    """,
        (limite,),
    )

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    lista = []
    for item in resultados:
        lista.append({"id": item[0], "nome": item[1], "total_vendido": item[2]})

    return lista


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

    lista = []
    for item in resultados:
        lista.append(
            {"id": item[0], "nome": item[1], "tamanho": item[2], "quantidade": item[3]}
        )

    return lista
