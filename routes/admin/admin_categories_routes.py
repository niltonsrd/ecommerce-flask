from flask import Blueprint, flash, render_template, request, redirect
from middlewares.auth import admin_required
from middlewares.security import IMAGE_EXTENSIONS, salvar_upload
from controllers.admin_controller import (
    listar_categorias_admin, criar_categoria_admin,
    obter_categoria_admin, editar_categoria_admin,
)

admin_categories_bp = Blueprint("admin_categories", __name__, url_prefix="/admin")


@admin_categories_bp.route("/categorias")
@admin_required
def categorias_admin():
    lista = listar_categorias_admin()
    return render_template("admin/categorias.html", categorias=lista)


@admin_categories_bp.route("/categorias/nova", methods=["GET", "POST"])
@admin_required
def nova_categoria():
    if request.method == "POST":
        nome = request.form["nome"]
        imagem = request.files.get("imagem")
        imagem_url = None
        if imagem and imagem.filename:
            try:
                imagem_url = salvar_upload(
                    imagem, "categoria", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect("/admin/categorias/nova")
        criar_categoria_admin(nome, imagem_url)
        return redirect("/admin/categorias")
    return render_template("admin/nova_categoria.html")


@admin_categories_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_categoria_page(id):
    categoria = obter_categoria_admin(id)
    if request.method == "POST":
        nome = request.form["nome"]
        imagem = request.files.get("imagem")
        imagem_url = categoria[2] if categoria and len(categoria) > 2 else None
        if imagem and imagem.filename:
            try:
                imagem_url = salvar_upload(
                    imagem, "categoria", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect(f"/admin/categorias/editar/{id}")
        editar_categoria_admin(id, nome, imagem_url)
        return redirect("/admin/categorias")
    return render_template("admin/editar_categoria.html", categoria=categoria)
