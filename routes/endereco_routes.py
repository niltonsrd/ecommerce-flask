from flask import Blueprint
from controllers.endereco_controller import (
    listar_enderecos_controller,
    novo_endereco_controller,
    definir_principal_controller,
    excluir_endereco_controller,
)

endereco_bp = Blueprint("endereco", __name__)


@endereco_bp.route("/enderecos")
def enderecos():
    return listar_enderecos_controller()


@endereco_bp.route("/enderecos/novo", methods=["GET", "POST"])
def novo_endereco():
    return novo_endereco_controller()


@endereco_bp.route("/enderecos/principal/<int:endereco_id>")
def definir_principal(endereco_id):
    return definir_principal_controller(endereco_id)


@endereco_bp.route("/enderecos/excluir/<int:endereco_id>")
def excluir_endereco(endereco_id):
    return excluir_endereco_controller(endereco_id)
