from flask import Blueprint, flash, render_template, request, redirect
from middlewares.auth import admin_required
from middlewares.security import IMAGE_EXTENSIONS, salvar_upload
from controllers.configuracao_controller import (
    obter_configuracoes_controller, salvar_configuracoes_controller,
)

admin_settings_bp = Blueprint("admin_settings", __name__, url_prefix="/admin")


@admin_settings_bp.route("/configuracoes", methods=["GET", "POST"])
@admin_required
def configuracoes_admin():
    config = obter_configuracoes_controller()
    if request.method == "POST":
        nome_loja = request.form["nome_loja"].strip()
        slogan = request.form["slogan"].strip()
        email_contato = request.form["email_contato"].strip()
        whatsapp = request.form["whatsapp"].strip()
        texto_rodape = request.form["texto_rodape"].strip()
        mostrar_credito = True if request.form.get("mostrar_credito") else False
        cor_primaria = request.form["cor_primaria"]
        cor_secundaria = request.form["cor_secundaria"]
        cidade_loja = request.form["cidade_loja"].strip()
        estado_loja = request.form["estado_loja"].strip().upper()
        cor_fundo = request.form["cor_fundo"]
        cor_fundo_secundario = request.form["cor_fundo_secundario"]
        cor_texto = request.form["cor_texto"]
        cor_texto_secundario = request.form["cor_texto_secundario"]

        logo_url = config[14] if config and len(config) > 14 else None
        background_url = config[16] if config and len(config) > 16 else None

        logo = request.files.get("logo")
        if logo and logo.filename:
            try:
                logo_url = salvar_upload(
                    logo, "logo", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect("/admin/configuracoes")

        background_file = request.files.get("background")
        if background_file and background_file.filename:
            try:
                background_url = salvar_upload(
                    background_file, "background", allowed_extensions=IMAGE_EXTENSIONS
                )
            except ValueError as exc:
                flash(str(exc), "erro")
                return redirect("/admin/configuracoes")

        salvar_configuracoes_controller(
            nome_loja, slogan, email_contato, whatsapp, texto_rodape,
            cor_primaria, cor_secundaria, cidade_loja, estado_loja,
            cor_fundo, cor_fundo_secundario, cor_texto, cor_texto_secundario,
            logo_url, mostrar_credito, background_url,
        )
        return redirect("/admin/configuracoes")

    return render_template("admin/configuracoes.html", config=config)
