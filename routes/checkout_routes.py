from flask import Blueprint
from controllers import checkout_controller

checkout_bp = Blueprint("checkout", __name__)

checkout_bp.route("/checkout", methods=["GET"])(checkout_controller.exibir_checkout)
checkout_bp.route("/checkout/finalizar", methods=["POST"])(
    checkout_controller.finalizar_checkout
)

checkout_bp.route("/checkout/pagamento/<int:pedido_id>", methods=["GET"])(
    checkout_controller.exibir_pagamento_checkout
)

checkout_bp.route("/checkout/sucesso/<int:pedido_id>", methods=["GET"])(
    checkout_controller.checkout_sucesso
)

checkout_bp.route("/checkout/validar-cupom", methods=["POST"])(
    checkout_controller.validar_cupom_ajax
)

checkout_bp.route("/checkout/salvar-endereco", methods=["POST"])(
    checkout_controller.salvar_endereco_ajax
)

checkout_bp.route("/checkout/pagamento/<int:pedido_id>/comprovante", methods=["POST"])(
    checkout_controller.enviar_comprovante_checkout
)
