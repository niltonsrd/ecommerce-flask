from repositories.favorito_repository import (
    adicionar_favorito,
    listar_favoritos,
    remover_favorito,
    verificar_favorito,
)


def favoritar(usuario_id, produto_id):

    ja_existe = verificar_favorito(usuario_id, produto_id)

    if ja_existe:
        return False

    adicionar_favorito(usuario_id, produto_id)
    return True


def meus_favoritos(usuario_id):
    return listar_favoritos(usuario_id)


def excluir_favorito(favorito_id, usuario_id):
    remover_favorito(favorito_id, usuario_id)
