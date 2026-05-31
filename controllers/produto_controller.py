from services.produto_service import (
    obter_produtos,
    obter_produto,
    obter_produtos_categoria,
    obter_imagem,
    obter_imagens_produto,
    obter_tamanhos_produto,
    buscar_produtos_filtrados,
    buscar_produtos_catalogo,
    total_produtos_filtrados,
)


def listar():
    return obter_produtos()


def detalhe(produto_id):
    return obter_produto(produto_id)


def listar_categoria(categoria_id):
    return obter_produtos_categoria(categoria_id)


def imagem_produto(produto_id):
    return obter_imagem(produto_id)


def imagens(produto_id):
    return obter_imagens_produto(produto_id)


def tamanhos(produto_id):
    return obter_tamanhos_produto(produto_id)


def filtrar(
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
    return buscar_produtos_filtrados(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id,
        ordem, limite, offset,
    )


def filtrar_catalogo(
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
    return buscar_produtos_catalogo(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id,
        ordem, limite, offset,
    )


def contar_filtrados(
    nome=None,
    categoria_id=None,
    preco_min=None,
    preco_max=None,
    marca_id=None,
    tamanho_id=None,
):
    return total_produtos_filtrados(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id,
    )
