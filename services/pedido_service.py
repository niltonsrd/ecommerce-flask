from repositories.pedido_repository import (
    listar_pedidos,
    atualizar_status,
    listar_pedidos_usuario,
    buscar_itens_pedido,
    buscar_status_pedido,
    buscar_itens_admin_pedido,
    buscar_pedido_admin_por_id,
    buscar_itens_detalhados_admin_pedido
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


def detalhe_pedido_admin(pedido_id):
    pedido = buscar_pedido_admin_por_id(pedido_id)

    if not pedido:
        return None

    itens = buscar_itens_detalhados_admin_pedido(pedido_id)

    pedido_dict = {
        "id": pedido[0],
        "usuario_id": pedido[1],
        "cliente_nome": pedido[2],
        "cliente_email": pedido[3],
        "cliente_telefone": pedido[4],
        "status": pedido[5],
        "valor_total": float(pedido[6] or 0),
        "subtotal": float(pedido[7] or 0),
        "desconto": float(pedido[8] or 0),
        "valor_frete": float(pedido[9] or 0),
        "forma_pagamento": pedido[10],
        "modalidade_entrega": pedido[11],
        "prazo_entrega": pedido[12],
        "observacoes": pedido[13],
        "data_pedido": pedido[14],
        "cep": pedido[15],
        "rua": pedido[16],
        "numero": pedido[17],
        "complemento": pedido[18],
        "bairro": pedido[19],
        "cidade": pedido[20],
        "estado": pedido[21],
        "cupom_codigo": pedido[22],
        "itens": [],
    }

    for item in itens:
        pedido_dict["itens"].append(
            {
                "id": item[0],
                "produto_id": item[1],
                "produto_nome": item[2],
                "quantidade": item[3],
                "preco": float(item[4] or 0),
                "tamanho_nome": item[5],
            }
        )

    return pedido_dict
