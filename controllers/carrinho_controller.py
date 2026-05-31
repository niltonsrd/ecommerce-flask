from services.carrinho_service import (
    adicionar,
    adicionar_anonimo,
    atualizar_quantidade,
    atualizar_quantidade_anonimo,
    buscar_mini_carrinho_anonimo,
    buscar_mini_carrinho_service,
    limpar,
    limpar_anonimo,
    listar,
    listar_anonimo,
    remover,
    remover_anonimo,
    total_itens,
    total_itens_anonimo,
)
from services.estoque_service import estoque_disponivel


def adicionar_produto(usuario_id, produto_id, tamanho_id, quantidade):
    if not estoque_disponivel(produto_id, tamanho_id, quantidade):
        return False

    return adicionar(usuario_id, produto_id, tamanho_id, quantidade)


def adicionar_produto_anonimo(carrinho, produto_id, tamanho_id, quantidade):
    return adicionar_anonimo(carrinho, produto_id, tamanho_id, quantidade)


def ver_carrinho(usuario_id):
    return listar(usuario_id)


def ver_carrinho_anonimo(carrinho):
    return listar_anonimo(carrinho)


def remover_produto(item_id, usuario_id=None):
    remover(item_id, usuario_id)


def remover_produto_anonimo(carrinho, item_id):
    return remover_anonimo(carrinho, item_id)


def atualizar_quantidade_produto(usuario_id, item_id, quantidade):
    return atualizar_quantidade(usuario_id, item_id, quantidade)


def atualizar_quantidade_produto_anonimo(carrinho, item_id, quantidade):
    return atualizar_quantidade_anonimo(carrinho, item_id, quantidade)


def limpar_carrinho(usuario_id):
    limpar(usuario_id)


def limpar_carrinho_anonimo():
    return limpar_anonimo()


def total_itens_carrinho(usuario_id):
    return total_itens(usuario_id)


def total_itens_carrinho_anonimo(carrinho):
    return total_itens_anonimo(carrinho)


def _montar_mini_response(itens):
    total = 0

    for item in itens:
        item["subtotal"] = float(item["preco"]) * int(item["quantidade"])
        total += item["subtotal"]

    return {"itens": itens, "total": total}


def obter_mini_carrinho(usuario_id):
    return _montar_mini_response(buscar_mini_carrinho_service(usuario_id))


def obter_mini_carrinho_anonimo(carrinho):
    return _montar_mini_response(buscar_mini_carrinho_anonimo(carrinho))
