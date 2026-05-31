from database.db import get_connection


def _item_from_row(row):
    subtotal = float(row[4]) * int(row[5])
    return {
        "id": row[0],
        "produto_id": row[1],
        "tamanho_id": row[2],
        "nome": row[3],
        "preco": float(row[4]),
        "quantidade": int(row[5]),
        "tamanho": row[6] or "-",
        "imagem": row[7],
        "estoque_disponivel": int(row[8] or 0),
        "subtotal": subtotal,
    }


def _buscar_estoque(cursor, produto_id, tamanho_id, bloquear=False):
    query = """
    SELECT quantidade, COALESCE(reservado, 0)
    FROM estoque
    WHERE produto_id = %s
      AND tamanho_id = %s
    """
    if bloquear:
        query += " FOR UPDATE"

    cursor.execute(query, (produto_id, tamanho_id))
    row = cursor.fetchone()
    if not row:
        return 0
    return max(int(row[0] or 0) - int(row[1] or 0), 0)


def verificar_disponibilidade(produto_id, tamanho_id):
    conn = get_connection()
    cursor = conn.cursor()

    disponivel = _buscar_estoque(cursor, produto_id, tamanho_id)

    cursor.close()
    conn.close()
    return disponivel


def adicionar_item(usuario_id, produto_id, tamanho_id, quantidade):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        produto_id = int(produto_id)
        tamanho_id = int(tamanho_id)
        quantidade = int(quantidade)
        if quantidade < 1:
            return False

        disponivel = _buscar_estoque(cursor, produto_id, tamanho_id, bloquear=True)

        cursor.execute(
            """
            SELECT quantidade
            FROM carrinho
            WHERE usuario_id = %s
              AND produto_id = %s
              AND tamanho_id = %s
            FOR UPDATE
            """,
            (usuario_id, produto_id, tamanho_id),
        )
        row = cursor.fetchone()
        quantidade_atual = int(row[0]) if row else 0

        if quantidade_atual + quantidade > disponivel:
            conn.rollback()
            return False

        cursor.execute(
            """
            INSERT INTO carrinho (usuario_id, produto_id, tamanho_id, quantidade)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (usuario_id, produto_id, tamanho_id)
            DO UPDATE SET quantidade = carrinho.quantidade + EXCLUDED.quantidade
            """,
            (usuario_id, produto_id, tamanho_id, quantidade),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def listar_carrinho(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        c.id,
        c.produto_id,
        c.tamanho_id,
        p.nome,
        p.preco,
        c.quantidade,
        t.nome,
        (
            SELECT pi.imagem_url
            FROM produto_imagens pi
            WHERE pi.produto_id = p.id
            ORDER BY pi.principal DESC, pi.ordem ASC, pi.id ASC
            LIMIT 1
        ) AS imagem_principal,
        GREATEST(e.quantidade - COALESCE(e.reservado, 0), 0) AS estoque_disponivel
    FROM carrinho c
    JOIN produtos p ON p.id = c.produto_id
    JOIN tamanhos t ON t.id = c.tamanho_id
    JOIN estoque e ON e.produto_id = c.produto_id AND e.tamanho_id = c.tamanho_id
    WHERE c.usuario_id = %s
      AND p.ativo = TRUE
    ORDER BY c.id DESC
    """

    cursor.execute(query, (usuario_id,))
    itens = [_item_from_row(row) for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return itens


def listar_carrinho_anonimo(itens_sessao):
    itens = [
        (int(item["produto_id"]), int(item["tamanho_id"]), int(item["quantidade"]))
        for item in itens_sessao
        if int(item.get("quantidade", 0)) > 0
    ]

    if not itens:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    values_sql = ", ".join(["(%s, %s, %s)"] * len(itens))
    params = []
    for produto_id, tamanho_id, quantidade in itens:
        params.extend([produto_id, tamanho_id, quantidade])

    query = f"""
    WITH carrinho_sessao(produto_id, tamanho_id, quantidade) AS (
        VALUES {values_sql}
    )
    SELECT
        (cs.produto_id::text || ':' || cs.tamanho_id::text) AS id,
        cs.produto_id,
        cs.tamanho_id,
        p.nome,
        p.preco,
        cs.quantidade,
        t.nome,
        (
            SELECT pi.imagem_url
            FROM produto_imagens pi
            WHERE pi.produto_id = p.id
            ORDER BY pi.principal DESC, pi.ordem ASC, pi.id ASC
            LIMIT 1
        ) AS imagem_principal,
        GREATEST(e.quantidade - COALESCE(e.reservado, 0), 0) AS estoque_disponivel
    FROM carrinho_sessao cs
    JOIN produtos p ON p.id = cs.produto_id
    JOIN tamanhos t ON t.id = cs.tamanho_id
    JOIN estoque e ON e.produto_id = cs.produto_id AND e.tamanho_id = cs.tamanho_id
    WHERE p.ativo = TRUE
    """

    cursor.execute(query, params)
    resultado = [_item_from_row(row) for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return resultado


def remover_item(item_id, usuario_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    if usuario_id is None:
        cursor.execute("DELETE FROM carrinho WHERE id = %s", (item_id,))
    else:
        cursor.execute(
            "DELETE FROM carrinho WHERE id = %s AND usuario_id = %s",
            (item_id, usuario_id),
        )

    conn.commit()
    cursor.close()
    conn.close()


def atualizar_quantidade_item(usuario_id, item_id, quantidade):
    quantidade = int(quantidade)
    if quantidade <= 0:
        remover_item(item_id, usuario_id)
        return True

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT produto_id, tamanho_id
            FROM carrinho
            WHERE id = %s AND usuario_id = %s
            FOR UPDATE
            """,
            (item_id, usuario_id),
        )
        row = cursor.fetchone()
        if not row:
            conn.rollback()
            return False

        disponivel = _buscar_estoque(cursor, row[0], row[1], bloquear=True)
        if quantidade > disponivel:
            conn.rollback()
            return False

        cursor.execute(
            """
            UPDATE carrinho
            SET quantidade = %s
            WHERE id = %s AND usuario_id = %s
            """,
            (quantidade, item_id, usuario_id),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def limpar_carrinho_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM carrinho WHERE usuario_id = %s", (usuario_id,))
    conn.commit()

    cursor.close()
    conn.close()


def contar_itens_carrinho(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(quantidade), 0)
        FROM carrinho
        WHERE usuario_id = %s
        """,
        (usuario_id,),
    )
    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return int(total or 0)


def buscar_mini_carrinho_repository(usuario_id):
    return listar_carrinho(usuario_id)[:5]
