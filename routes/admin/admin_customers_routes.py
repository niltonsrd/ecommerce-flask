from flask import Blueprint, render_template

from controllers.cliente_controller import listar_clientes_admin_controller
from middlewares.auth import admin_required

admin_customers_bp = Blueprint("admin_customers", __name__, url_prefix="/admin")


@admin_customers_bp.route("/clientes")
@admin_required
def clientes_admin():
    clientes = listar_clientes_admin_controller()
    return render_template("admin/clientes.html", clientes=clientes)
