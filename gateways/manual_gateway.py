from gateways.pagamento_gateway import PagamentoGateway


class ManualGateway(PagamentoGateway):
    def criar_pagamento(self, pedido_id, metodo, valor):
        metodo = (metodo or "").upper()

        if metodo == "PIX":
            return {
                "gateway": "MANUAL",
                "metodo": "PIX",
                "status": "AGUARDANDO_PAGAMENTO",
                "pedido_id": pedido_id,
                "valor": float(valor),
                "instrucao": "Realize o pagamento manualmente usando a chave PIX da loja.",
            }

        if metodo == "BOLETO":
            return {
                "gateway": "MANUAL",
                "metodo": "BOLETO",
                "status": "AGUARDANDO_PAGAMENTO",
                "pedido_id": pedido_id,
                "valor": float(valor),
                "instrucao": "Pagamento por boleto em modo manual.",
            }

        if metodo == "CARTAO":
            return {
                "gateway": "MANUAL",
                "metodo": "CARTAO",
                "status": "AGUARDANDO_PAGAMENTO",
                "pedido_id": pedido_id,
                "valor": float(valor),
                "instrucao": "Pagamento por cartão em modo manual.",
            }

        raise ValueError("Método de pagamento inválido.")
