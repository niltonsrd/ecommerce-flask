from repositories.estoque_repository import (listar_tamanhos, 
salvar_estoque,
verificar_estoque,
reduzir_estoque,
confirmar_reserva_pedido,
liberar_reserva_pedido,
)


def obter_tamanhos():

    return listar_tamanhos()


def adicionar_estoque(produto_id, tamanho_id, quantidade):

    salvar_estoque(produto_id, tamanho_id, quantidade)


def estoque_disponivel(produto_id, tamanho_id, quantidade=1):

    estoque = verificar_estoque(produto_id, tamanho_id)

    if estoque and estoque[0] >= int(quantidade):
        return True

    return False


def diminuir_estoque(produto_id, tamanho_id, quantidade):

    reduzir_estoque(produto_id, tamanho_id, quantidade)


def confirmar_estoque_pedido(pedido_id):
    return confirmar_reserva_pedido(pedido_id)


def liberar_estoque_pedido(pedido_id):
    return liberar_reserva_pedido(pedido_id)
