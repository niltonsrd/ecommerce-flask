from flask import Blueprint, redirect, render_template

from controllers.admin_controller import alterar_status, pedidos
from controllers.pedido_controller import ver_detalhe_pedido_admin
from middlewares.auth import admin_required
from repositories.pagamento_repository import (
    atualizar_status_pagamento,
    buscar_pagamento_por_pedido,
)
from repositories.pedido_repository import atualizar_status as atualizar_status_pedido_db
from services.estoque_service import confirmar_estoque_pedido, liberar_estoque_pedido

admin_orders_bp = Blueprint("admin_orders", __name__, url_prefix="/admin")


@admin_orders_bp.route("/pedidos")
@admin_required
def pedidos_admin():
    lista = pedidos()
    return render_template(
        "admin/pedidos.html",
        pedidos=lista,
        buscar_pagamento_por_pedido=buscar_pagamento_por_pedido,
    )


@admin_orders_bp.route("/pedidos/<int:pedido_id>")
@admin_required
def detalhe_pedido_admin_page(pedido_id):
    pedido = ver_detalhe_pedido_admin(pedido_id)
    if not pedido:
        return "Pedido não encontrado", 404
    return render_template("admin/pedido_detalhe.html", pedido=pedido)


@admin_orders_bp.route("/pedidos/<int:pedido_id>/comprovante")
@admin_required
def comprovante_pedido_admin_page(pedido_id):
    pedido = ver_detalhe_pedido_admin(pedido_id)
    if not pedido:
        return "Pedido não encontrado", 404
    return render_template("admin/pedido_comprovante.html", pedido=pedido)


@admin_orders_bp.route("/pedidos/status/<int:id>/<status>")
@admin_required
def atualizar_status_pedido(id, status):
    status_validos = {
        "AGUARDANDO_PAGAMENTO",
        "PAGO",
        "EM_SEPARACAO",
        "ENVIADO",
        "ENTREGUE",
        "CANCELADO",
        "FALHA_PAGAMENTO",
    }
    if status not in status_validos:
        return "Status inválido", 400

    if status == "PAGO":
        confirmar_estoque_pedido(id)
    elif status in {"CANCELADO", "FALHA_PAGAMENTO"}:
        liberar_estoque_pedido(id)

    alterar_status(id, status)
    return redirect("/admin/pedidos")


@admin_orders_bp.route("/pagamentos/aprovar/<int:pedido_id>")
@admin_required
def aprovar_pagamento(pedido_id):
    pagamento = buscar_pagamento_por_pedido(pedido_id)
    if pagamento:
        confirmar_estoque_pedido(pedido_id)
        atualizar_status_pagamento(pagamento["id"], "PAGO")
        atualizar_status_pedido_db(pedido_id, "PAGO")
    return redirect("/admin/pedidos")


@admin_orders_bp.route("/pagamentos/recusar/<int:pedido_id>")
@admin_required
def recusar_pagamento(pedido_id):
    pagamento = buscar_pagamento_por_pedido(pedido_id)
    if pagamento:
        liberar_estoque_pedido(pedido_id)
        atualizar_status_pagamento(pagamento["id"], "RECUSADO")
        atualizar_status_pedido_db(pedido_id, "FALHA_PAGAMENTO")
    return redirect("/admin/pedidos")
