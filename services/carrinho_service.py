from repositories.carrinho_repository import (
    adicionar_item,
    listar_carrinho,
    remover_item,
    contar_itens_carrinho,
    buscar_mini_carrinho_repository,
)


def adicionar(usuario_id, produto_id, tamanho_id, quantidade):

    adicionar_item(usuario_id, produto_id, tamanho_id, quantidade)


def listar(usuario_id):

    return listar_carrinho(usuario_id)


def remover(item_id):

    remover_item(item_id)

def total_itens(usuario_id):

    return contar_itens_carrinho(usuario_id)


def buscar_mini_carrinho_service(usuario_id):
    return buscar_mini_carrinho_repository(usuario_id)
