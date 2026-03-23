from flask import Blueprint, session, redirect, render_template
from controllers.favorito_controller import (
    adicionar_favorito_controller,
    listar_favoritos_controller,
    remover_favorito_controller,
)

favorito_bp = Blueprint("favorito", __name__)


@favorito_bp.route("/favoritar/<int:produto_id>")
def favoritar_produto(produto_id):

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    resultado = adicionar_favorito_controller(usuario_id, produto_id)

    if not resultado:
        return redirect("/favoritos")

    return redirect("/favoritos")


@favorito_bp.route("/favoritos")
def favoritos_page():

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    favoritos = listar_favoritos_controller(usuario_id)

    return render_template("loja/favoritos.html", favoritos=favoritos, pagina_conta="favoritos")


@favorito_bp.route("/remover-favorito/<int:favorito_id>")
def remover_favorito_page(favorito_id):

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    remover_favorito_controller(favorito_id, usuario_id)

    return redirect("/favoritos")
