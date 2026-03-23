from services.favorito_service import favoritar, meus_favoritos, excluir_favorito


def adicionar_favorito_controller(usuario_id, produto_id):
    return favoritar(usuario_id, produto_id)


def listar_favoritos_controller(usuario_id):
    return meus_favoritos(usuario_id)


def remover_favorito_controller(favorito_id, usuario_id):
    excluir_favorito(favorito_id, usuario_id)
