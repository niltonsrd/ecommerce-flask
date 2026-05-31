from flask import Blueprint, render_template, request, redirect
from middlewares.auth import admin_required
from controllers.frete_controller import (
    listar_fretes_controller, obter_frete_controller,
    criar_frete_controller, editar_frete_controller, excluir_frete_controller,
)
from controllers.modalidade_entrega_controller import (
    listar_modalidades_controller, obter_modalidade_controller,
    criar_modalidade_controller, editar_modalidade_controller, excluir_modalidade_controller,
)

admin_delivery_bp = Blueprint("admin_delivery", __name__, url_prefix="/admin")


@admin_delivery_bp.route("/fretes")
@admin_required
def fretes_admin():
    fretes = listar_fretes_controller()
    return render_template("admin/fretes.html", fretes=fretes)


@admin_delivery_bp.route("/fretes/novo", methods=["GET", "POST"])
@admin_required
def novo_frete_admin():
    if request.method == "POST":
        nome_regiao = request.form["nome_regiao"]
        cep_inicio = request.form["cep_inicio"]
        cep_fim = request.form["cep_fim"]
        valor = request.form["valor"]
        prazo_dias = request.form["prazo_dias"]
        ativo = request.form["ativo"] == "true"
        criar_frete_controller(nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo)
        return redirect("/admin/fretes")
    return render_template("admin/novo_frete.html")


@admin_delivery_bp.route("/fretes/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_frete_admin(id):
    if request.method == "POST":
        nome_regiao = request.form["nome_regiao"]
        cep_inicio = request.form["cep_inicio"]
        cep_fim = request.form["cep_fim"]
        valor = request.form["valor"]
        prazo_dias = request.form["prazo_dias"]
        ativo = request.form["ativo"] == "true"
        editar_frete_controller(id, nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo)
        return redirect("/admin/fretes")
    frete = obter_frete_controller(id)
    return render_template("admin/editar_frete.html", frete=frete)


@admin_delivery_bp.route("/fretes/excluir/<int:id>")
@admin_required
def excluir_frete_admin(id):
    excluir_frete_controller(id)
    return redirect("/admin/fretes")


@admin_delivery_bp.route("/modalidades-entrega")
@admin_required
def modalidades_entrega_admin():
    modalidades = listar_modalidades_controller()
    return render_template("admin/modalidades_entrega.html", modalidades=modalidades)


@admin_delivery_bp.route("/modalidades-entrega/nova", methods=["GET", "POST"])
@admin_required
def nova_modalidade_entrega_admin():
    if request.method == "POST":
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        cidade = request.form["cidade"] or None
        estado = request.form["estado"] or None
        valor = request.form["valor"]
        prazo_horas = request.form["prazo_horas"] or None
        prazo_dias = request.form["prazo_dias"] or None
        ativo = request.form["ativo"] == "true"
        criar_modalidade_controller(nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo)
        return redirect("/admin/modalidades-entrega")
    return render_template("admin/nova_modalidade_entrega.html")


@admin_delivery_bp.route("/modalidades-entrega/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def editar_modalidade_entrega_admin(id):
    if request.method == "POST":
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        cidade = request.form["cidade"] or None
        estado = request.form["estado"] or None
        valor = request.form["valor"]
        prazo_horas = request.form["prazo_horas"] or None
        prazo_dias = request.form["prazo_dias"] or None
        ativo = request.form["ativo"] == "true"
        editar_modalidade_controller(id, nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo)
        return redirect("/admin/modalidades-entrega")
    modalidade = obter_modalidade_controller(id)
    return render_template("admin/editar_modalidade_entrega.html", modalidade=modalidade)


@admin_delivery_bp.route("/modalidades-entrega/excluir/<int:id>")
@admin_required
def excluir_modalidade_entrega_admin(id):
    excluir_modalidade_controller(id)
    return redirect("/admin/modalidades-entrega")
