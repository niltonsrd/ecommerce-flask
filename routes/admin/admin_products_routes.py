from flask import Blueprint, flash, render_template, request, redirect
from middlewares.auth import admin_required
from middlewares.security import IMAGE_EXTENSIONS, salvar_upload
from repositories.admin_repository import salvar_imagem
from controllers.admin_controller import (
    listar, criar, deletar, produto, editar,
    listar_imagens, adicionar_imagem, excluir_imagem, definir_principal,
    tamanhos, estoque, listar_categorias_admin,
)
from services.marca_service import marcas

admin_products_bp = Blueprint("admin_products", __name__, url_prefix="/admin")


@admin_products_bp.route("/produtos")
@admin_required
def produtos():
    lista_produtos = listar()
    return render_template("admin/produtos.html", produtos=lista_produtos)


@admin_products_bp.route("/produtos/novo", methods=["GET", "POST"])
@admin_required
def novo_produto():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        categoria_id = request.form["categoria"]
        marca_id = request.form["marca"]
        imagem = request.files.get("imagem")
        nome_arquivo = None
        if imagem and imagem.filename:
            try:
                nome_arquivo = salvar_upload(
                    imagem, "produto", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect("/admin/produtos/novo")
        produto_id = criar(nome, descricao, preco, categoria_id, marca_id)
        if nome_arquivo:
            salvar_imagem(produto_id, nome_arquivo)
        return redirect("/admin/produtos")
    categorias_lista = listar_categorias_admin()
    lista_marcas = marcas()
    return render_template("admin/novo_produto.html", categorias=categorias_lista, marcas=lista_marcas)


@admin_products_bp.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_produto_page(id):
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        categoria_id = request.form["categoria"]
        marca_id = request.form["marca"]
        ativo = request.form["ativo"] == "true"
        editar(id, nome, descricao, preco, categoria_id, marca_id, ativo)
        return redirect("/admin/produtos")
    produto_dados = produto(id)
    categorias_lista = listar_categorias_admin()
    lista_marcas = marcas()
    return render_template("admin/editar_produto.html", produto=produto_dados, categorias=categorias_lista, marcas=lista_marcas)


@admin_products_bp.route("/produtos/deletar/<int:id>")
@admin_required
def deletar_produto(id):
    deletar(id)
    return redirect("/admin/produtos")


@admin_products_bp.route("/produtos/<int:id>/estoque", methods=["GET", "POST"])
@admin_required
def estoque_produto(id):
    if request.method == "POST":
        tamanho_id = request.form["tamanho"]
        quantidade = request.form["quantidade"]
        estoque(id, tamanho_id, quantidade)
        return redirect("/admin/produtos")
    lista_tamanhos = tamanhos()
    return render_template("admin/estoque_produto.html", tamanhos=lista_tamanhos, produto_id=id)


@admin_products_bp.route("/produtos/<int:id>/imagens", methods=["GET", "POST"])
@admin_required
def gerenciar_imagens(id):
    if request.method == "POST":
        imagem = request.files.get("imagem")
        if imagem and imagem.filename:
            try:
                nome = salvar_upload(
                    imagem, "produto", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect(f"/admin/produtos/{id}/imagens")
            adicionar_imagem(id, nome)
    imagens_lista = listar_imagens(id)
    return render_template("admin/imagens_produto.html", imagens=imagens_lista, produto_id=id)


@admin_products_bp.route("/produtos/imagem/excluir/<int:id>/<int:produto_id>")
@admin_required
def excluir_imagem_produto(id, produto_id):
    excluir_imagem(id)
    return redirect(f"/admin/produtos/{produto_id}/imagens")


@admin_products_bp.route("/produtos/imagem/principal/<int:id>/<int:produto_id>")
@admin_required
def definir_principal_produto(id, produto_id):
    definir_principal(produto_id, id)
    return redirect(f"/admin/produtos/{produto_id}/imagens")
