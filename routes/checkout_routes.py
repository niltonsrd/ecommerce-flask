from flask import Blueprint
from controllers import checkout_controller
from middlewares.auth import login_required

checkout_bp = Blueprint("checkout", __name__)

checkout_bp.route("/checkout", methods=["GET"])(login_required(checkout_controller.exibir_checkout))
checkout_bp.route("/checkout/finalizar", methods=["POST"])(login_required(checkout_controller.finalizar_checkout))
checkout_bp.route("/checkout/pagamento/<int:pedido_id>", methods=["GET"])(login_required(checkout_controller.exibir_pagamento_checkout))
checkout_bp.route("/checkout/sucesso/<int:pedido_id>", methods=["GET"])(login_required(checkout_controller.checkout_sucesso))
checkout_bp.route("/checkout/validar-cupom", methods=["POST"])(login_required(checkout_controller.validar_cupom_ajax))
checkout_bp.route("/checkout/salvar-endereco", methods=["POST"])(login_required(checkout_controller.salvar_endereco_ajax))
checkout_bp.route("/checkout/pagamento/<int:pedido_id>/comprovante", methods=["POST"])(login_required(checkout_controller.enviar_comprovante_checkout))
