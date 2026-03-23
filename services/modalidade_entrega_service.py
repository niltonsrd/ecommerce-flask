from repositories.modalidade_entrega_repository import (
    listar_modalidades_admin,
    buscar_modalidade_por_id,
    buscar_modalidades_checkout,
    criar_modalidade,
    atualizar_modalidade,
    excluir_modalidade,
)


def listar_modalidades():
    return listar_modalidades_admin()


def obter_modalidade(modalidade_id):
    return buscar_modalidade_por_id(modalidade_id)


def modalidades_checkout(cidade):
    return buscar_modalidades_checkout(cidade)


def nova_modalidade(nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo):
    criar_modalidade(nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo)


def editar_modalidade(
    modalidade_id, nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
):
    atualizar_modalidade(
        modalidade_id, nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
    )


def deletar_modalidade(modalidade_id):
    excluir_modalidade(modalidade_id)
