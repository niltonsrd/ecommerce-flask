from database.db import get_connection


def listar_produtos_admin():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        p.id,
        p.nome,
        p.preco,
        c.nome,
        m.nome,
        p.descricao,
        p.ativo,

        (
            SELECT pi.imagem_url
            FROM produto_imagens pi
            WHERE pi.produto_id = p.id
            AND pi.principal = TRUE
            ORDER BY pi.ordem ASC
            LIMIT 1
        ) AS imagem_principal,

        COALESCE((
            SELECT SUM(e.quantidade)
            FROM estoque e
            WHERE e.produto_id = p.id
        ),0) AS estoque_total,

        (
            SELECT STRING_AGG(
                t.nome || ': ' || e.quantidade,
                ' | ' ORDER BY t.nome
            )
            FROM estoque e
            JOIN tamanhos t ON t.id = e.tamanho_id
            WHERE e.produto_id = p.id
        ) AS estoque_por_tamanho

    FROM produtos p
    LEFT JOIN categorias c ON c.id = p.categoria_id
    LEFT JOIN marcas m ON m.id = p.marca_id
    ORDER BY p.id DESC
    """

    cursor.execute(query)

    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return produtos


def criar_produto(nome, descricao, preco, categoria_id, marca_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO produtos (nome, descricao, preco, categoria_id, marca_id)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """

    cursor.execute(query, (nome, descricao, preco, categoria_id, marca_id))

    produto_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return produto_id


def deletar_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM produtos WHERE id = %s"

    cursor.execute(query, (produto_id,))

    conn.commit()

    cursor.close()
    conn.close()


def buscar_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome,
        descricao,
        preco,
        categoria_id,
        marca_id,
        ativo
    FROM produtos
    WHERE id = %s
    """

    cursor.execute(query, (produto_id,))

    produto = cursor.fetchone()

    cursor.close()
    conn.close()

    return produto


def atualizar_produto(
    produto_id, nome, descricao, preco, categoria_id, marca_id, ativo
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE produtos
    SET nome = %s,
        descricao = %s,
        preco = %s,
        categoria_id = %s,
        marca_id = %s,
        ativo = %s
    WHERE id = %s
    """

    cursor.execute(
        query, (nome, descricao, preco, categoria_id, marca_id, ativo, produto_id)
    )

    conn.commit()

    cursor.close()
    conn.close()


def salvar_imagem(produto_id, imagem):

    conn = get_connection()
    cursor = conn.cursor()

    query_verifica = """
    SELECT COUNT(*)
    FROM produto_imagens
    WHERE produto_id = %s
    """

    cursor.execute(query_verifica, (produto_id,))
    total_imagens = cursor.fetchone()[0]

    principal = total_imagens == 0
    ordem = total_imagens + 1

    query = """
    INSERT INTO produto_imagens (produto_id, imagem_url, principal, ordem)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (produto_id, imagem, principal, ordem))

    conn.commit()

    cursor.close()
    conn.close()


def listar_imagens_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, imagem_url, principal, ordem
    FROM produto_imagens
    WHERE produto_id = %s
    ORDER BY principal DESC, ordem ASC
    """

    cursor.execute(query, (produto_id,))
    imagens = cursor.fetchall()

    cursor.close()
    conn.close()

    return imagens


def adicionar_imagem_produto(produto_id, imagem_url):

    conn = get_connection()
    cursor = conn.cursor()

    query_ordem = """
    SELECT COALESCE(MAX(ordem),0) + 1
    FROM produto_imagens
    WHERE produto_id = %s
    """

    cursor.execute(query_ordem, (produto_id,))
    ordem = cursor.fetchone()[0]

    query = """
    INSERT INTO produto_imagens (produto_id, imagem_url, principal, ordem)
    VALUES (%s, %s, FALSE, %s)
    """

    cursor.execute(query, (produto_id, imagem_url, ordem))

    conn.commit()
    cursor.close()
    conn.close()


def remover_imagem_produto(imagem_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM produto_imagens WHERE id = %s", (imagem_id,))

    conn.commit()
    cursor.close()
    conn.close()


def definir_imagem_principal(produto_id, imagem_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE produto_imagens SET principal = FALSE WHERE produto_id = %s",
        (produto_id,),
    )

    cursor.execute(
        "UPDATE produto_imagens SET principal = TRUE WHERE id = %s", (imagem_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()
