from database.db import get_connection


def adicionar_item(usuario_id, produto_id, tamanho_id, quantidade):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO carrinho (usuario_id, produto_id, tamanho_id, quantidade)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (usuario_id, produto_id, tamanho_id, quantidade))

    conn.commit()

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
              AND pi.principal = TRUE
            ORDER BY pi.ordem ASC, pi.id ASC
            LIMIT 1
        ) AS imagem_principal
    FROM carrinho c
    JOIN produtos p ON p.id = c.produto_id
    LEFT JOIN tamanhos t ON t.id = c.tamanho_id
    WHERE c.usuario_id = %s
    """

    cursor.execute(query, (usuario_id,))

    itens = cursor.fetchall()

    cursor.close()
    conn.close()

    return itens


def remover_item(item_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM carrinho WHERE id = %s"

    cursor.execute(query, (item_id,))

    conn.commit()

    cursor.close()
    conn.close()


def contar_itens_carrinho(usuario_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COALESCE(SUM(quantidade), 0)
    FROM carrinho
    WHERE usuario_id = %s
    """

    cursor.execute(query, (usuario_id,))

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


def buscar_mini_carrinho_repository(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        c.id,
        p.nome,
        p.preco,
        c.quantidade,
        t.nome AS tamanho,
        (
            SELECT pi.imagem_url
            FROM produto_imagens pi
            WHERE pi.produto_id = p.id
            ORDER BY pi.principal DESC, pi.id ASC
            LIMIT 1
        ) AS imagem
    FROM carrinho c
    JOIN produtos p ON p.id = c.produto_id
    LEFT JOIN tamanhos t ON t.id = c.tamanho_id
    WHERE c.usuario_id = %s
    ORDER BY c.id DESC
    LIMIT 5
    """

    cursor.execute(query, (usuario_id,))
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    itens = []

    for item in resultados:
        itens.append(
            {
                "id": item[0],
                "nome": item[1],
                "preco": float(item[2]),
                "quantidade": item[3],
                "tamanho": item[4] if item[4] else "-",
                "imagem": item[5],
            }
        )

    return itens
