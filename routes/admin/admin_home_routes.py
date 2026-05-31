from flask import Blueprint, flash, render_template, request, redirect
from middlewares.auth import admin_required
from middlewares.security import IMAGE_EXTENSIONS, salvar_upload
from controllers.home_bloco_controller import (
    listar_blocos_home_controller, obter_bloco_home_controller,
    criar_bloco_home_controller, editar_bloco_home_controller, excluir_bloco_home_controller,
)

admin_home_bp = Blueprint("admin_home", __name__, url_prefix="/admin")


@admin_home_bp.route("/home-blocos")
@admin_required
def home_blocos_admin():
    blocos = listar_blocos_home_controller()
    return render_template("admin/home_blocos.html", blocos=blocos)


@admin_home_bp.route("/home-blocos/novo", methods=["GET", "POST"])
@admin_required
def novo_bloco_home_admin():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        tipo_bloco = request.form["tipo_bloco"]
        layout = request.form["layout"]
        titulo = request.form["titulo"].strip()
        subtitulo = request.form["subtitulo"].strip()
        descricao = request.form["descricao"].strip()
        texto_botao = request.form["texto_botao"].strip()
        link_botao = request.form["link_botao"].strip()
        texto_botao_secundario = request.form["texto_botao_secundario"].strip()
        link_botao_secundario = request.form["link_botao_secundario"].strip()
        cor_fundo = request.form["cor_fundo"] or None
        cor_texto = request.form["cor_texto"] or None
        alinhamento_texto = request.form["alinhamento_texto"]
        ordem = int(request.form["ordem"])
        ativo = request.form["ativo"] == "true"
        imagem = request.files.get("imagem")
        imagem_url = None
        if imagem and imagem.filename:
            try:
                imagem_url = salvar_upload(
                    imagem, "home", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect("/admin/home-blocos/novo")
        criar_bloco_home_controller(nome, tipo_bloco, layout, titulo, subtitulo, descricao, imagem_url, texto_botao, link_botao, texto_botao_secundario, link_botao_secundario, cor_fundo, cor_texto, alinhamento_texto, ordem, ativo)
        return redirect("/admin/home-blocos")
    return render_template("admin/novo_home_bloco.html")


@admin_home_bp.route("/home-blocos/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_bloco_home_admin(id):
    bloco = obter_bloco_home_controller(id)
    if request.method == "POST":
        nome = request.form["nome"].strip()
        tipo_bloco = request.form["tipo_bloco"]
        layout = request.form["layout"]
        titulo = request.form["titulo"].strip()
        subtitulo = request.form["subtitulo"].strip()
        descricao = request.form["descricao"].strip()
        texto_botao = request.form["texto_botao"].strip()
        link_botao = request.form["link_botao"].strip()
        texto_botao_secundario = request.form["texto_botao_secundario"].strip()
        link_botao_secundario = request.form["link_botao_secundario"].strip()
        cor_fundo = request.form["cor_fundo"] or None
        cor_texto = request.form["cor_texto"] or None
        alinhamento_texto = request.form["alinhamento_texto"]
        ordem = int(request.form["ordem"])
        ativo = request.form["ativo"] == "true"
        imagem_url = bloco[7] if bloco and len(bloco) > 7 else None
        imagem = request.files.get("imagem")
        if imagem and imagem.filename:
            try:
                imagem_url = salvar_upload(
                    imagem, "home", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect(f"/admin/home-blocos/editar/{id}")
        editar_bloco_home_controller(id, nome, tipo_bloco, layout, titulo, subtitulo, descricao, imagem_url, texto_botao, link_botao, texto_botao_secundario, link_botao_secundario, cor_fundo, cor_texto, alinhamento_texto, ordem, ativo)
        return redirect("/admin/home-blocos")
    return render_template("admin/editar_home_bloco.html", bloco=bloco)


@admin_home_bp.route("/home-blocos/excluir/<int:id>")
@admin_required
def excluir_bloco_home_admin(id):
    excluir_bloco_home_controller(id)
    return redirect("/admin/home-blocos")


@admin_home_bp.route("/banners")
@admin_required
def banners_admin_page():
    from controllers.banner_controller import listar_banners_admin_controller
    banners = listar_banners_admin_controller()
    return render_template("admin/banners.html", banners=banners)


@admin_home_bp.route("/banners/novo", methods=["GET", "POST"])
@admin_required
def novo_banner_admin():
    from controllers.banner_controller import criar_banner_controller
    if request.method == "POST":
        titulo = request.form["titulo"]
        subtitulo = request.form["subtitulo"]
        link = request.form["link"]
        ativo = request.form["ativo"] == "true"
        ordem = request.form["ordem"]
        imagem = request.files.get("imagem")
        imagem_url = None
        if imagem and imagem.filename:
            try:
                imagem_url = salvar_upload(
                    imagem, "banner", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect("/admin/banners/novo")
        criar_banner_controller(titulo, subtitulo, imagem_url, link, ativo, ordem)
        return redirect("/admin/banners")
    return render_template("admin/novo_banner.html")


@admin_home_bp.route("/banners/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_banner_admin(id):
    from controllers.banner_controller import obter_banner_controller, editar_banner_controller
    banner = obter_banner_controller(id)
    if request.method == "POST":
        titulo = request.form["titulo"]
        subtitulo = request.form["subtitulo"]
        link = request.form["link"]
        ativo = request.form["ativo"] == "true"
        ordem = request.form["ordem"]
        imagem = request.files.get("imagem")
        imagem_url = banner[3] if banner and len(banner) > 3 else None
        if imagem and imagem.filename:
            try:
                imagem_url = salvar_upload(
                    imagem, "banner", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect(f"/admin/banners/editar/{id}")
        editar_banner_controller(id, titulo, subtitulo, imagem_url, link, ativo, ordem)
        return redirect("/admin/banners")
    return render_template("admin/editar_banner.html", banner=banner)


@admin_home_bp.route("/banners/excluir/<int:id>")
@admin_required
def excluir_banner_admin(id):
    from controllers.banner_controller import excluir_banner_controller
    excluir_banner_controller(id)
    return redirect("/admin/banners")
