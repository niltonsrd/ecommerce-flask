from flask import Blueprint
from middlewares.auth import login_required
from controllers.endereco_controller import (
    listar_enderecos_controller,
    novo_endereco_controller,
    definir_principal_controller,
    excluir_endereco_controller,
)

endereco_bp = Blueprint("endereco", __name__)


@endereco_bp.route("/enderecos")
@login_required
def enderecos():
    return listar_enderecos_controller()


@endereco_bp.route("/enderecos/novo", methods=["GET", "POST"])
@login_required
def novo_endereco():
    return novo_endereco_controller()


@endereco_bp.route("/enderecos/principal/<int:endereco_id>")
@login_required
def definir_principal(endereco_id):
    return definir_principal_controller(endereco_id)


@endereco_bp.route("/enderecos/excluir/<int:endereco_id>")
@login_required
def excluir_endereco(endereco_id):
    return excluir_endereco_controller(endereco_id)
