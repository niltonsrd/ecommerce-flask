from services.avaliacao_service import (
    salvar_avaliacao,
    obter_avaliacoes,
    obter_resumo_avaliacoes,
    obter_avaliacao_usuario,
)


def criar_avaliacao_controller(produto_id, usuario_id, nota, comentario):
    salvar_avaliacao(produto_id, usuario_id, nota, comentario)


def listar_avaliacoes_controller(produto_id):
    return obter_avaliacoes(produto_id)


def resumo_avaliacoes_controller(produto_id):
    return obter_resumo_avaliacoes(produto_id)


def avaliacao_usuario_controller(produto_id, usuario_id):
    return obter_avaliacao_usuario(produto_id, usuario_id)
