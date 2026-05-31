from flask import Blueprint, render_template, request, redirect
from middlewares.auth import admin_required
from controllers.cupom_admin_controller import (
    listar_cupons_controller, obter_cupom_controller,
    criar_cupom_controller, editar_cupom_controller, excluir_cupom_controller,
)

admin_coupons_bp = Blueprint("admin_coupons", __name__, url_prefix="/admin")


@admin_coupons_bp.route("/cupons")
@admin_required
def cupons_admin():
    cupons = listar_cupons_controller()
    return render_template("admin/cupons.html", cupons=cupons)


@admin_coupons_bp.route("/cupons/novo", methods=["GET", "POST"])
@admin_required
def novo_cupom_admin():
    if request.method == "POST":
        codigo = request.form["codigo"]
        tipo = request.form["tipo"]
        valor = request.form["valor"]
        valor_minimo = request.form["valor_minimo"]
        limite_uso = request.form["limite_uso"]
        ativo = request.form["ativo"] == "true"
        data_inicio = request.form["data_inicio"] or None
        data_fim = request.form["data_fim"] or None
        criar_cupom_controller(codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim)
        return redirect("/admin/cupons")
    return render_template("admin/novo_cupom.html")


@admin_coupons_bp.route("/cupons/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_cupom_admin(id):
    if request.method == "POST":
        codigo = request.form["codigo"]
        tipo = request.form["tipo"]
        valor = request.form["valor"]
        valor_minimo = request.form["valor_minimo"]
        limite_uso = request.form["limite_uso"]
        ativo = request.form["ativo"] == "true"
        data_inicio = request.form["data_inicio"] or None
        data_fim = request.form["data_fim"] or None
        editar_cupom_controller(id, codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim)
        return redirect("/admin/cupons")
    cupom = obter_cupom_controller(id)
    return render_template("admin/editar_cupom.html", cupom=cupom)


@admin_coupons_bp.route("/cupons/excluir/<int:id>")
@admin_required
def excluir_cupom_admin(id):
    excluir_cupom_controller(id)
    return redirect("/admin/cupons")
