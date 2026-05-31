from flask import Blueprint, session, redirect, render_template
from middlewares.auth import login_required
from controllers.pedido_controller import (
    listar_meus_pedidos,
    ver_detalhe_pedido,
)

pedido_bp = Blueprint("pedido", __name__)


@pedido_bp.route("/finalizar-pedido")
def finalizar():
    return redirect("/checkout")


@pedido_bp.route("/meus-pedidos")
@login_required
def meus_pedidos_page():
    usuario_id = session.get("usuario_id")
    pedidos = listar_meus_pedidos(usuario_id)
    return render_template("loja/meus_pedidos.html", pedidos=pedidos, pagina_conta="pedidos")


@pedido_bp.route("/meu-pedido/<int:pedido_id>")
@login_required
def detalhe_pedido_page(pedido_id):
    usuario_id = session.get("usuario_id")
    itens = ver_detalhe_pedido(pedido_id, usuario_id)
    if not itens:
        return "Pedido não encontrado"
    return render_template("loja/detalhe_pedido.html", itens=itens)
