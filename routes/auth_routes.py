from flask import Blueprint, render_template, request, redirect, session

from middlewares.auth import login_required, guest_required
from middlewares.security import (
    IMAGE_EXTENSIONS,
    login_rate_limit,
    reset_login_rate_limit,
    salvar_upload,
    validar_arquivo,
)
from services.carrinho_service import SESSION_CART_KEY, mesclar_carrinho_anonimo
from controllers.auth_controller import (
    cadastrar_usuario,
    login_usuario,
    atualizar_dados_usuario,
    atualizar_avatar_usuario,
    obter_usuario_por_id,
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
@guest_required
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        cadastrar_usuario(nome, email, senha)
        return redirect("/login")
    return render_template("auth/cadastro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@guest_required
@login_rate_limit
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form["email"]
    senha = request.form["senha"]
    usuario = login_usuario(email, senha)

    if usuario:
        carrinho_anonimo = session.get(SESSION_CART_KEY, {})
        session.clear()
        session["usuario_id"] = usuario[0]
        session["usuario_nome"] = usuario[1]
        session["usuario_email"] = usuario[2]
        session["usuario_tipo"] = usuario[4] or "cliente"
        session["usuario_telefone"] = usuario[6] or ""
        session["usuario_cpf"] = usuario[7] or ""
        session["usuario_data_nascimento"] = usuario[8] or ""

        foto_usuario = None
        if len(usuario) > 5 and isinstance(usuario[5], str):
            foto_usuario = usuario[5]
        session["usuario_foto"] = foto_usuario

        if carrinho_anonimo:
            mesclar_carrinho_anonimo(usuario[0], carrinho_anonimo)
            session.pop(SESSION_CART_KEY, None)

        reset_login_rate_limit()

        if session["usuario_tipo"] == "admin":
            return redirect("/admin")
        return redirect("/produtos")

    return render_template("auth/login.html", erro="Email ou senha inválidos")


@auth_bp.route("/minha-conta", methods=["GET", "POST"])
@login_required
def minha_conta():
    if request.method == "POST":
        return redirect("/configuracoes-conta")
    return render_template("loja/minha_conta.html", pagina_conta="visao_geral")


@auth_bp.route("/configuracoes-conta", methods=["GET", "POST"])
@login_required
def configuracoes_conta():
    usuario_id = session.get("usuario_id")
    erro = None
    sucesso = None

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        cpf = request.form.get("cpf", "").strip()
        data_nascimento = request.form.get("data_nascimento")
        foto = request.files.get("foto")

        try:
            atualizar_dados_usuario(usuario_id, nome, telefone, cpf, data_nascimento)
            session["usuario_nome"] = nome

            if foto and foto.filename:
                valido, msg_erro = validar_arquivo(foto, allowed_extensions=IMAGE_EXTENSIONS)
                if not valido:
                    raise ValueError(msg_erro)

                foto_url = salvar_upload(
                    foto,
                    f"perfil_{usuario_id}",
                    subdiretorio="perfis",
                    allowed_extensions=IMAGE_EXTENSIONS,
                )

                atualizar_avatar_usuario(usuario_id, foto_url)
                session["usuario_foto"] = foto_url

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
