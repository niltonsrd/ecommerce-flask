from repositories.carrinho_repository import (
    adicionar_item,
    atualizar_quantidade_item,
    buscar_mini_carrinho_repository,
    contar_itens_carrinho,
    limpar_carrinho_usuario,
    listar_carrinho,
    listar_carrinho_anonimo,
    remover_item,
    verificar_disponibilidade,
)


SESSION_CART_KEY = "carrinho_anonimo"


def _cart_key(produto_id, tamanho_id):
    return f"{int(produto_id)}:{int(tamanho_id)}"


def _normalizar_carrinho_sessao(carrinho):
    if not carrinho:
        return {}
    valores = carrinho.values() if isinstance(carrinho, dict) else carrinho
    return {
        _cart_key(item.get("produto_id"), item.get("tamanho_id")): {
            "produto_id": int(item.get("produto_id")),
            "tamanho_id": int(item.get("tamanho_id")),
            "quantidade": int(item.get("quantidade", 0)),
        }
        for item in valores
        if int(item.get("quantidade", 0)) > 0
    }


def adicionar(usuario_id, produto_id, tamanho_id, quantidade):
    return adicionar_item(usuario_id, produto_id, tamanho_id, quantidade)


def adicionar_anonimo(carrinho, produto_id, tamanho_id, quantidade):
    carrinho = _normalizar_carrinho_sessao(carrinho)
    produto_id = int(produto_id)
    tamanho_id = int(tamanho_id)
    quantidade = int(quantidade)

    if quantidade < 1:
        return False, carrinho

    key = _cart_key(produto_id, tamanho_id)
    atual = int(carrinho.get(key, {}).get("quantidade", 0))
    disponivel = verificar_disponibilidade(produto_id, tamanho_id)

    if atual + quantidade > disponivel:
        return False, carrinho

    carrinho[key] = {
        "produto_id": produto_id,
        "tamanho_id": tamanho_id,
        "quantidade": atual + quantidade,
    }
    return True, carrinho


def mesclar_carrinho_anonimo(usuario_id, carrinho):
    carrinho = _normalizar_carrinho_sessao(carrinho)
    for item in carrinho.values():
        adicionar(
            usuario_id,
            item["produto_id"],
            item["tamanho_id"],
            item["quantidade"],
        )


def listar(usuario_id):
    return listar_carrinho(usuario_id)


def listar_anonimo(carrinho):
    carrinho = _normalizar_carrinho_sessao(carrinho)
    return listar_carrinho_anonimo(carrinho.values())


def remover(item_id, usuario_id=None):
    remover_item(item_id, usuario_id)


def remover_anonimo(carrinho, item_id):
    carrinho = _normalizar_carrinho_sessao(carrinho)
    carrinho.pop(str(item_id), None)
    return carrinho


def atualizar_quantidade(usuario_id, item_id, quantidade):
    return atualizar_quantidade_item(usuario_id, item_id, quantidade)


def atualizar_quantidade_anonimo(carrinho, item_id, quantidade):
    carrinho = _normalizar_carrinho_sessao(carrinho)
    quantidade = int(quantidade)

    if str(item_id) not in carrinho:
        return False, carrinho

    if quantidade <= 0:
        carrinho.pop(str(item_id), None)
        return True, carrinho

    item = carrinho[str(item_id)]
    disponivel = verificar_disponibilidade(item["produto_id"], item["tamanho_id"])
    if quantidade > disponivel:
        return False, carrinho

    item["quantidade"] = quantidade
    carrinho[str(item_id)] = item
    return True, carrinho


def limpar(usuario_id):
    limpar_carrinho_usuario(usuario_id)


def limpar_anonimo():
    return {}


def total_itens(usuario_id):
    return contar_itens_carrinho(usuario_id)


def total_itens_anonimo(carrinho):
    carrinho = _normalizar_carrinho_sessao(carrinho)
    return sum(int(item["quantidade"]) for item in carrinho.values())


def buscar_mini_carrinho_service(usuario_id):
    return buscar_mini_carrinho_repository(usuario_id)


def buscar_mini_carrinho_anonimo(carrinho):
    return listar_anonimo(carrinho)[:5]
