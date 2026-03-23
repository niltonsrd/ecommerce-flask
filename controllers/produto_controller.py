from flask import request, render_template
from services.produto_service import (obter_produtos, 
obter_produto, 
obter_produtos_categoria,
obter_imagem,
obter_imagens_produto,
obter_tamanhos_produto,
buscar_produtos_filtrados,
total_produtos_filtrados
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


from services.produto_service import buscar_produtos_filtrados, total_produtos_filtrados


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


def contar_filtrados(
    nome=None,
    categoria_id=None,
    preco_min=None,
    preco_max=None,
    marca_id=None,
    tamanho_id=None,
):
    return total_produtos_filtrados(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id
    )


def listar_produtos_controller():

    nome = request.args.get("q")
    categoria_id = request.args.get("categoria")
    preco_min = request.args.get("preco_min")
    preco_max = request.args.get("preco_max")
    marca_id = request.args.get("marca")
    tamanho_id = request.args.get("tamanho")
    ordem = request.args.get("ordem")

    pagina = int(request.args.get("pagina", 1))
    limite = 12
    offset = (pagina - 1) * limite

    produtos = buscar_produtos_filtrados(
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

    total = total_produtos_filtrados(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id
    )

    total_paginas = (total // limite) + (1 if total % limite > 0 else 0)

    return render_template(
        "produtos_lista.html",
        produtos=produtos,
        pagina=pagina,
        total_paginas=total_paginas,
    )
