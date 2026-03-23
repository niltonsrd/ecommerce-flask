from repositories.produto_repository import (
listar_produtos, 
buscar_produto_por_id,
produtos_por_categoria,
buscar_imagem_produto,
buscar_imagens_produto,
tamanhos_produto,
filtrar_produtos,
contar_produtos_filtrados
)


def obter_produtos():

    return listar_produtos()

def obter_produto(produto_id):

    return buscar_produto_por_id(produto_id)

def obter_produtos_categoria(categoria_id):

    return produtos_por_categoria(categoria_id)

def obter_imagem(produto_id):

    return buscar_imagem_produto(produto_id)


def obter_imagens_produto(produto_id):
    return buscar_imagens_produto(produto_id)


def obter_tamanhos_produto(produto_id):

    return tamanhos_produto(produto_id)


def buscar_produtos_filtrados(
    nome=None,
    categoria_id=None,
    preco_min=None,
    preco_max=None,
    marca_id=None,
    tamanho_id=None,
):
    return filtrar_produtos(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id
    )

from repositories.produto_repository import filtrar_produtos, contar_produtos_filtrados


def buscar_produtos_filtrados(
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
    return filtrar_produtos(
        nome,
        categoria_id,
        preco_min,
        preco_max,
        marca_id,
        tamanho_id,
        ordem,
        limite,
        offset,
    )


def total_produtos_filtrados(
    nome=None,
    categoria_id=None,
    preco_min=None,
    preco_max=None,
    marca_id=None,
    tamanho_id=None,
):
    return contar_produtos_filtrados(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id
    )
