import os
import uuid
from flask import Blueprint, render_template, request, redirect, session, current_app
from werkzeug.utils import secure_filename

from controllers.auth_controller import (
    cadastrar_usuario,
    login_usuario,
    atualizar_dados_usuario,
    atualizar_avatar_usuario,
    obter_usuario_por_id,
)

auth_bp = Blueprint("auth", __name__)


def arquivo_permitido(filename):
    extensoes_permitidas = {"png", "jpg", "jpeg", "webp"}
    return (
        "." in filename and filename.rsplit(".", 1)[1].lower() in extensoes_permitidas
    )


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        cadastrar_usuario(nome, email, senha)

        return redirect("/login")

    return render_template("auth/cadastro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET" and session.get("usuario_id"):
        if session.get("usuario_tipo") == "admin":
            return redirect("/admin")
        return redirect("/produtos")

    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = login_usuario(email, senha)

        print("USUARIO:", usuario)

        if usuario:
            for i, campo in enumerate(usuario):
                print(f"Índice {i}: {campo} | Tipo: {type(campo)}")

            session.clear()
            session["usuario_id"] = usuario[0]
            session["usuario_nome"] = usuario[1]
            session["usuario_email"] = usuario[2]
            session["usuario_tipo"] = usuario[4] or "cliente"

            foto_usuario = None
            if len(usuario) > 5 and isinstance(usuario[5], str):
                foto_usuario = usuario[5]

            session["usuario_foto"] = foto_usuario

            if session["usuario_tipo"] == "admin":
                return redirect("/admin")

            return redirect("/produtos")

        return "Email ou senha inválidos"

    return render_template("auth/login.html")


@auth_bp.route("/minha-conta")
def minha_conta():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    return render_template(
        "loja/minha_conta.html",
        pagina_conta="visao_geral",
    )


@auth_bp.route("/configuracoes-conta", methods=["GET", "POST"])
def configuracoes_conta():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    erro = None
    sucesso = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        foto = request.files.get("foto")

        try:
            atualizar_dados_usuario(usuario_id, nome)
            session["usuario_nome"] = nome

            if foto and foto.filename:
                if not arquivo_permitido(foto.filename):
                    raise ValueError("Envie uma imagem PNG, JPG, JPEG ou WEBP.")

                nome_seguro = secure_filename(foto.filename)
                extensao = nome_seguro.rsplit(".", 1)[1].lower()
                nome_arquivo = f"perfil_{usuario_id}_{uuid.uuid4().hex}.{extensao}"

                pasta_destino = os.path.join(
                    current_app.static_folder, "uploads", "perfis"
                )
                os.makedirs(pasta_destino, exist_ok=True)

                caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
                foto.save(caminho_arquivo)

                atualizar_avatar_usuario(usuario_id, f"perfis/{nome_arquivo}")
                session["usuario_foto"] = f"perfis/{nome_arquivo}"

            sucesso = "Seus dados foram atualizados com sucesso."

        except ValueError as e:
            erro = str(e)

    usuario = obter_usuario_por_id(usuario_id)

    return render_template(
        "loja/configuracoes_conta.html",
        pagina_conta="configuracoes",
        erro=erro,
        sucesso=sucesso,
        usuario=usuario,
    )


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
