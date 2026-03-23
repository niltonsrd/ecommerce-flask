from repositories.pedido_repository import (
    listar_pedidos,
    atualizar_status,
    listar_pedidos_usuario,
    buscar_itens_pedido,
    buscar_status_pedido,
    buscar_itens_admin_pedido,
)
from services.estoque_service import diminuir_estoque
from repositories.pagamento_repository import (
    buscar_pagamento_por_pedido,
    atualizar_status_pagamento,
)


def pedidos_admin():
    return listar_pedidos()


def mudar_status(pedido_id, status):
    status_atual = buscar_status_pedido(pedido_id)

    if not status_atual:
        return False

    status_atual = status_atual[0]

    if status == status_atual:
        return True

    if status == "PAGO" and status_atual != "PAGO":
        itens = buscar_itens_admin_pedido(pedido_id)

        for item in itens:
            produto_id = item[0]
            tamanho_id = item[1]
            quantidade = item[2]

            diminuir_estoque(produto_id, tamanho_id, quantidade)

        pagamento = buscar_pagamento_por_pedido(pedido_id)
        if pagamento:
            atualizar_status_pagamento(pagamento["id"], "APROVADO")

    if status in ["CANCELADO", "FALHA_PAGAMENTO"]:
        pagamento = buscar_pagamento_por_pedido(pedido_id)
        if pagamento:
            atualizar_status_pagamento(pagamento["id"], "CANCELADO")

    atualizar_status(pedido_id, status)
    return True


def meus_pedidos(usuario_id):
    return listar_pedidos_usuario(usuario_id)


def detalhe_pedido(pedido_id, usuario_id):
    return buscar_itens_pedido(pedido_id, usuario_id)
