from database.db import get_connection


def buscar_itens_carrinho(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            c.id,
            c.produto_id,
            c.tamanho_id,
            c.quantidade,
            p.nome,
            p.preco,
            COALESCE(
                (
                    SELECT imagem_url
                    FROM produto_imagens pi
                    WHERE pi.produto_id = p.id
                    ORDER BY pi.principal DESC, pi.ordem ASC, pi.id ASC
                    LIMIT 1
                ),
                ''
            ) AS imagem_url,
            t.nome AS tamanho_nome,
            e.quantidade AS estoque_disponivel
        FROM carrinho c
        INNER JOIN produtos p ON p.id = c.produto_id
        INNER JOIN tamanhos t ON t.id = c.tamanho_id
        INNER JOIN estoque e ON e.produto_id = c.produto_id AND e.tamanho_id = c.tamanho_id
        WHERE c.usuario_id = %s
          AND p.ativo = TRUE
        ORDER BY c.id DESC
    """
    cursor.execute(query, (usuario_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    itens = []
    for row in rows:
        subtotal = float(row[3]) * float(row[5])
        itens.append(
            {
                "carrinho_id": row[0],
                "produto_id": row[1],
                "tamanho_id": row[2],
                "quantidade": row[3],
                "nome": row[4],
                "preco": float(row[5]),
                "imagem_url": row[6],
                "tamanho_nome": row[7],
                "estoque_disponivel": row[8],
                "subtotal": subtotal,
            }
        )

    return itens


def buscar_cupom_por_codigo(codigo):
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
            ativo,
            data_inicio,
            data_fim
        FROM cupons
        WHERE UPPER(codigo) = UPPER(%s)
        LIMIT 1
    """
    cursor.execute(query, (codigo,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "codigo": row[1],
        "tipo_desconto": row[2],
        "valor_desconto": float(row[3]),
        "valor_minimo": float(row[4]) if row[4] is not None else 0.0,
        "limite_uso": row[5],
        "ativo": row[6],
        "data_inicio": row[7],
        "data_fim": row[8],
    }


def listar_modalidades_ativas():
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
    WHERE ativo = TRUE
    ORDER BY valor ASC, id ASC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    modalidades = []
    for row in rows:
        prazo = "Prazo a combinar"

        if row[6]:
            prazo = f"Até {row[6]} hora(s)"
        elif row[7] is not None:
            if int(row[7]) == 0:
                prazo = "Disponível imediatamente"
            else:
                prazo = f"{row[7]} dia(s)"

        modalidades.append(
            {
                "id": row[0],
                "nome": row[1],
                "tipo": row[2],
                "cidade": row[3],
                "estado": row[4],
                "valor": float(row[5]),
                "prazo": prazo,
                "ativo": row[8],
            }
        )

    return modalidades


def buscar_modalidade_entrega_por_id(modalidade_id):
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
    WHERE id = %s AND ativo = TRUE
    LIMIT 1
    """

    cursor.execute(query, (modalidade_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    prazo = "Prazo a combinar"

    if row[6]:
        prazo = f"Até {row[6]} hora(s)"
    elif row[7] is not None:
        if int(row[7]) == 0:
            prazo = "Disponível imediatamente"
        else:
            prazo = f"{row[7]} dia(s)"

    return {
        "id": row[0],
        "nome": row[1],
        "tipo": row[2],
        "cidade": row[3],
        "estado": row[4],
        "valor": float(row[5]),
        "prazo": prazo,
        "ativo": row[8],
    }


def criar_pedido(
    usuario_id,
    endereco_id,
    cupom_id,
    subtotal,
    desconto,
    valor_frete,
    valor_total,
    modalidade_entrega_id,
    modalidade_entrega,
    prazo_entrega,
    forma_pagamento,
    observacoes,
):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO pedidos (
        usuario_id,
        endereco_id,
        cupom_id,
        subtotal,
        desconto,
        valor_frete,
        valor_total,
        modalidade_entrega_id,
        modalidade_entrega,
        prazo_entrega,
        forma_pagamento,
        observacoes,
        status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'AGUARDANDO_PAGAMENTO')
    RETURNING id
"""

    cursor.execute(
        query,
        (
            usuario_id,
            endereco_id,
            cupom_id,
            subtotal,
            desconto,
            valor_frete,
            valor_total,
            modalidade_entrega_id,
            modalidade_entrega,
            prazo_entrega,
            forma_pagamento,
            observacoes,
        ),
    )

    pedido_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return pedido_id


def adicionar_item_pedido(pedido_id, produto_id, tamanho_id, quantidade, preco):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO pedido_itens (pedido_id, produto_id, tamanho_id, quantidade, preco)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (pedido_id, produto_id, tamanho_id, quantidade, preco))
    conn.commit()

    cursor.close()
    conn.close()


def limpar_carrinho_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM carrinho WHERE usuario_id = %s"
    cursor.execute(query, (usuario_id,))
    conn.commit()

    cursor.close()
    conn.close()


def buscar_pedido_por_id(pedido_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.id,
            p.usuario_id,
            p.endereco_id,
            p.cupom_id,
            p.subtotal,
            p.desconto,
            p.valor_frete,
            p.valor_total,
            p.modalidade_entrega_id,
            p.modalidade_entrega,
            p.prazo_entrega,
            p.forma_pagamento,
            p.observacoes,
            p.status,
            p.criado_em
        FROM pedidos p
        WHERE p.id = %s AND p.usuario_id = %s
        LIMIT 1
    """
    cursor.execute(query, (pedido_id, usuario_id))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "usuario_id": row[1],
        "endereco_id": row[2],
        "cupom_id": row[3],
        "subtotal": float(row[4]),
        "desconto": float(row[5]),
        "valor_frete": float(row[6]),
        "valor_total": float(row[7]),
        "modalidade_entrega_id": row[8],
        "modalidade_entrega": row[9],
        "prazo_entrega": row[10],
        "forma_pagamento": row[11],
        "observacoes": row[12],
        "status": row[13],
        "criado_em": row[14],
    }
