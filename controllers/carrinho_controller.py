from services.carrinho_service import adicionar, listar, remover, total_itens, buscar_mini_carrinho_service
from services.estoque_service import estoque_disponivel


def adicionar_produto(usuario_id, produto_id, tamanho_id, quantidade):
    if not estoque_disponivel(produto_id, tamanho_id):
        return False

    adicionar(usuario_id, produto_id, tamanho_id, quantidade)
    return True


def ver_carrinho(usuario_id):
    return listar(usuario_id)


def remover_produto(item_id):
    remover(item_id)


def total_itens_carrinho(usuario_id):
    return total_itens(usuario_id)


def obter_mini_carrinho(usuario_id):
    itens = buscar_mini_carrinho_service(usuario_id)

    total = 0

    for item in itens:
        item["subtotal"] = float(item["preco"]) * int(item["quantidade"])
        total += item["subtotal"]

    return {"itens": itens, "total": total}
