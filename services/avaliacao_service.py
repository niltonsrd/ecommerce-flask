from repositories.avaliacao_repository import (
    criar_avaliacao,
    listar_avaliacoes_produto,
    resumo_avaliacoes_produto,
    buscar_avaliacao_usuario,
)


def salvar_avaliacao(produto_id, usuario_id, nota, comentario):
    criar_avaliacao(produto_id, usuario_id, nota, comentario)


def obter_avaliacoes(produto_id):
    return listar_avaliacoes_produto(produto_id)


def obter_resumo_avaliacoes(produto_id):
    return resumo_avaliacoes_produto(produto_id)


def obter_avaliacao_usuario(produto_id, usuario_id):
    return buscar_avaliacao_usuario(produto_id, usuario_id)
