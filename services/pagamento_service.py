from gateways.manual_gateway import ManualGateway
from middlewares.security import salvar_upload
from repositories import pagamento_repository
from repositories.pagamento_repository import salvar_comprovante_pagamento


GATEWAY_ATIVO = "MANUAL"
EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "pdf"}


def arquivo_permitido(nome_arquivo):
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS
    )


def enviar_comprovante_pagamento(pedido_id, arquivo, observacao_cliente=None):
    if not arquivo or not arquivo.filename:
        raise Exception("Selecione um arquivo de comprovante.")

    try:
        url_salva = salvar_upload(
            arquivo,
            f"comprovante_pedido_{pedido_id}",
            subdiretorio="comprovantes",
            allowed_extensions=EXTENSOES_PERMITIDAS,
        )
    except ValueError as exc:
        raise Exception(str(exc)) from exc

    salvar_comprovante_pagamento(
        pedido_id=pedido_id,
        comprovante_url=url_salva,
        observacao_cliente=observacao_cliente,
    )

    return url_salva


def obter_gateway():
    if GATEWAY_ATIVO == "MANUAL":
        return ManualGateway()

    raise ValueError("Gateway de pagamento não configurado.")


def criar_pagamento_inicial(pedido_id, metodo, valor):
    gateway = obter_gateway()
    pagamento = gateway.criar_pagamento(pedido_id=pedido_id, metodo=metodo, valor=valor)

    pagamento_id = pagamento_repository.criar_pagamento(
        pedido_id=pedido_id,
        metodo=pagamento.get("metodo"),
        valor=pagamento.get("valor"),
        status=pagamento.get("status"),
        gateway=pagamento.get("gateway"),
        referencia_externa=pagamento.get("payment_id"),
        detalhes=pagamento.get("instrucao"),
    )

    pagamento["id"] = pagamento_id
    return pagamento
