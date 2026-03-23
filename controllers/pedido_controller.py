from services.pedido_service import (
    pedidos_admin,
    mudar_status,
    meus_pedidos,
    detalhe_pedido,
)


def pedidos():
    return pedidos_admin()


def alterar_status(pedido_id, status):
    return mudar_status(pedido_id, status)


def listar_meus_pedidos(usuario_id):
    return meus_pedidos(usuario_id)


def ver_detalhe_pedido(pedido_id, usuario_id):
    return detalhe_pedido(pedido_id, usuario_id)
