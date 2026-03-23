from database.db import get_connection


def listar_produtos():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        p.id,
        p.nome,
        p.preco,
        COALESCE(
            (
                SELECT pi.imagem_url
                FROM produto_imagens pi
                WHERE pi.produto_id = p.id
                ORDER BY pi.principal DESC, pi.ordem ASC, pi.id ASC
                LIMIT 1
            ),
            ''
        ) AS imagem
    FROM produtos p
    WHERE p.ativo = TRUE
    ORDER BY p.id DESC
    """

    cursor.execute(query)

    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return produtos


def buscar_produto_por_id(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        p.id,
        p.nome,
        p.descricao,
        p.preco,
        c.nome,
        m.nome
    FROM produtos p
    LEFT JOIN categorias c ON c.id = p.categoria_id
    LEFT JOIN marcas m ON m.id = p.marca_id
    WHERE p.id = %s
    """

    cursor.execute(query, (produto_id,))

    produto = cursor.fetchone()

    cursor.close()
    conn.close()

    return produto


def produtos_por_categoria(categoria_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        nome,
        preco
    FROM produtos
    WHERE categoria_id = %s
    AND ativo = TRUE
    """

    cursor.execute(query, (categoria_id,))

    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return produtos


def buscar_imagem_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT imagem_url
    FROM produto_imagens
    WHERE produto_id = %s
      AND principal = TRUE
    ORDER BY ordem ASC, id ASC
    LIMIT 1
    """

    cursor.execute(query, (produto_id,))

    imagem = cursor.fetchone()

    cursor.close()
    conn.close()

    return imagem


def buscar_imagens_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        imagem_url,
        principal,
        ordem
    FROM produto_imagens
    WHERE produto_id = %s
    ORDER BY principal DESC, ordem ASC, id ASC
    """

    cursor.execute(query, (produto_id,))

    imagens = cursor.fetchall()

    cursor.close()
    conn.close()

    return imagens


def tamanhos_produto(produto_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        t.id,
        t.nome,
        e.quantidade
    FROM estoque e
    JOIN tamanhos t ON t.id = e.tamanho_id
    WHERE e.produto_id = %s
    AND e.quantidade > 0
    """

    cursor.execute(query, (produto_id,))

    tamanhos = cursor.fetchall()

    cursor.close()
    conn.close()

    return tamanhos


def filtrar_produtos(
    nome=None,
    categoria_id=None,
    preco_min=None,
    preco_max=None,
    marca_id=None,
    tamanho_id=None,
    ordem=None,
    limite=12,
    offset=0,
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT DISTINCT
        p.id,
        p.nome,
        p.preco
    FROM produtos p
    """

    if tamanho_id:
        query += """
        JOIN estoque e ON e.produto_id = p.id
        """

    query += " WHERE p.ativo = TRUE"

    params = []

    if nome:
        query += " AND p.nome ILIKE %s"
        params.append(f"%{nome}%")

    if categoria_id:
        query += " AND p.categoria_id = %s"
        params.append(categoria_id)

    if marca_id:
        query += " AND p.marca_id = %s"
        params.append(marca_id)

    if tamanho_id:
        query += " AND e.tamanho_id = %s AND e.quantidade > 0"
        params.append(tamanho_id)

    if preco_min:
        query += " AND p.preco >= %s"
        params.append(preco_min)

    if preco_max:
        query += " AND p.preco <= %s"
        params.append(preco_max)

    if ordem == "menor_preco":
        query += " ORDER BY p.preco ASC"
    elif ordem == "maior_preco":
        query += " ORDER BY p.preco DESC"
    else:
        query += " ORDER BY p.id DESC"

    query += " LIMIT %s OFFSET %s"
    params.append(limite)
    params.append(offset)

    cursor.execute(query, params)

    produtos = cursor.fetchall()

    cursor.close()
    conn.close()

    return produtos


def contar_produtos_filtrados(
    nome=None,
    categoria_id=None,
    preco_min=None,
    preco_max=None,
    marca_id=None,
    tamanho_id=None,
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(DISTINCT p.id)
    FROM produtos p
    """

    if tamanho_id:
        query += """
        JOIN estoque e ON e.produto_id = p.id
        """

    query += " WHERE p.ativo = TRUE"

    params = []

    if nome:
        query += " AND p.nome ILIKE %s"
        params.append(f"%{nome}%")

    if categoria_id:
        query += " AND p.categoria_id = %s"
        params.append(categoria_id)

    if marca_id:
        query += " AND p.marca_id = %s"
        params.append(marca_id)

    if tamanho_id:
        query += " AND e.tamanho_id = %s AND e.quantidade > 0"
        params.append(tamanho_id)

    if preco_min:
        query += " AND p.preco >= %s"
        params.append(preco_min)

    if preco_max:
        query += " AND p.preco <= %s"
        params.append(preco_max)

    cursor.execute(query, params)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


def buscar_produtos(filtro=None, categoria_slug=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        p.id,
        p.nome,
        p.preco,
        c.nome AS categoria,
        COALESCE(
            (
                SELECT imagem_url
                FROM produto_imagens pi
                WHERE pi.produto_id = p.id
                ORDER BY pi.principal DESC, pi.ordem ASC
                LIMIT 1
            ),
            ''
        ) AS imagem
    FROM produtos p
    LEFT JOIN categorias c ON c.id = p.categoria_id
    WHERE p.ativo = TRUE
    """

    params = []

    if filtro:
        query += " AND LOWER(p.nome) LIKE LOWER(%s)"
        params.append(f"%{filtro}%")

    if categoria_slug:
        query += " AND LOWER(c.nome) = LOWER(%s)"
        params.append(categoria_slug)

    query += " ORDER BY p.id DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    produtos = []

    for row in rows:
        produtos.append(
            {
                "id": row[0],
                "nome": row[1],
                "preco": float(row[2]),
                "categoria": row[3],
                "imagem": row[4],
            }
        )

    return produtos
