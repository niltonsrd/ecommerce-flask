from flask import Blueprint, render_template, request, redirect, session
from controllers.produto_controller import (
    listar,
    detalhe,
    listar_categoria,
    imagem_produto,
    imagens,
    tamanhos,
    filtrar,
    contar_filtrados
)
from services.categoria_service import categorias
from services.marca_service import marcas
from services.tamanho_service import listar_tamanhos
from controllers.avaliacao_controller import (
    criar_avaliacao_controller,
    listar_avaliacoes_controller,
    resumo_avaliacoes_controller,
    avaliacao_usuario_controller,
)


produto_bp = Blueprint("produtos", __name__)


@produto_bp.route("/produtos")
def produtos():

    nome = request.args.get("q")
    categoria_id = request.args.get("categoria")
    marca_id = request.args.get("marca")
    preco_min = request.args.get("preco_min")
    preco_max = request.args.get("preco_max")
    tamanho_id = request.args.get("tamanho")
    ordem = request.args.get("ordem", "recentes")
    pagina = request.args.get("pagina", 1, type=int)

    limite = 6
    offset = (pagina - 1) * limite

    lista = filtrar(
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

    total_produtos = contar_filtrados(
        nome, categoria_id, preco_min, preco_max, marca_id, tamanho_id
    )

    total_paginas = (total_produtos + limite - 1) // limite

    produtos = []

    for p in lista:
        produto_id = p[0]

        img = imagem_produto(produto_id)
        imagem = img[0] if img else None

        lista_imagens_bruta = imagens(produto_id)
        lista_imagens = (
            [item[1] for item in lista_imagens_bruta] if lista_imagens_bruta else []
        )

        lista_tamanhos_bruta = tamanhos(produto_id)
        lista_tamanhos = []

        for t in lista_tamanhos_bruta:
            lista_tamanhos.append({"id": t[0], "nome": t[1], "estoque": t[2]})

        produtos.append(
            {
                "id": produto_id,
                "nome": p[1],
                "preco": float(p[2]),
                "imagem": imagem,
                "imagens": lista_imagens,
                "tamanhos": lista_tamanhos,
            }
        )

    lista_categorias = categorias()
    lista_marcas = marcas()
    lista_tamanhos = listar_tamanhos()

    return render_template(
        "loja/produtos.html",
        produtos=produtos,
        categorias=lista_categorias,
        marcas=lista_marcas,
        tamanhos=lista_tamanhos,
        filtro_q=nome,
        filtro_categoria=categoria_id,
        filtro_marca=marca_id,
        filtro_preco_min=preco_min,
        filtro_preco_max=preco_max,
        filtro_tamanho=tamanho_id,
        filtro_ordem=ordem,
        pagina_atual=pagina,
        total_paginas=total_paginas,
    )


@produto_bp.route("/produto/<int:id>")
def produto(id):

    dados = detalhe(id)
    lista_tamanhos = tamanhos(id)
    lista_imagens = imagens(id)
    lista_avaliacoes = listar_avaliacoes_controller(id)
    resumo = resumo_avaliacoes_controller(id)

    usuario_id = session.get("usuario_id")
    minha_avaliacao = None

    if usuario_id:
        minha_avaliacao = avaliacao_usuario_controller(id, usuario_id)

    return render_template(
        "loja/produto.html",
        produto=dados,
        tamanhos=lista_tamanhos,
        imagens=lista_imagens,
        avaliacoes=lista_avaliacoes,
        resumo_avaliacoes=resumo,
        minha_avaliacao=minha_avaliacao,
    )


@produto_bp.route("/produto/<int:id>/avaliar", methods=["POST"])
def avaliar_produto(id):

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    nota = int(request.form["nota"])
    comentario = request.form["comentario"]

    criar_avaliacao_controller(id, usuario_id, nota, comentario)

    return redirect(f"/produto/{id}")


@produto_bp.route("/categoria/<int:id>")
def categoria(id):

    lista = listar_categoria(id)

    produtos = []

    for p in lista:
        produto_id = p[0]

        # imagem principal
        img = imagem_produto(produto_id)
        imagem = img[0] if img else None

        # TODAS as imagens
        imgs = imagens(produto_id)
        lista_imagens = [i[1] for i in imgs] if imgs else []

        # tamanhos com estoque
        tam = tamanhos(produto_id)
        lista_tamanhos = (
            [
                {
                    "id": t[0],
                    "nome": t[1],
                    "estoque": t[2],
                }
                for t in tam
            ]
            if tam
            else []
        )

        produtos.append(
            {
                "id": produto_id,
                "nome": p[1],
                "preco": float(p[2]),
                "imagem": imagem,
                "imagens": lista_imagens,
                "tamanhos": lista_tamanhos,
            }
        )

    lista_categorias = categorias()
    lista_marcas = marcas()
    lista_tamanhos = listar_tamanhos()

    return render_template(
        "loja/produtos.html",
        produtos=produtos,
        categorias=lista_categorias,
        marcas=lista_marcas,
        tamanhos=lista_tamanhos,
        filtro_q=None,
        filtro_categoria=str(id),
        filtro_marca=None,
        filtro_preco_min=None,
        filtro_preco_max=None,
        filtro_tamanho=None,
        filtro_ordem="recentes",
        pagina_atual=1,
        total_paginas=1,
    )
