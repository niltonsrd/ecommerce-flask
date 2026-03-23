from services.modalidade_entrega_service import (
    listar_modalidades,
    obter_modalidade,
    modalidades_checkout,
    nova_modalidade,
    editar_modalidade,
    deletar_modalidade,
)


def listar_modalidades_controller():
    return listar_modalidades()


def obter_modalidade_controller(modalidade_id):
    return obter_modalidade(modalidade_id)


def listar_modalidades_regiao_controller(cidade, estado=None):
    return modalidades_checkout(cidade)


def criar_modalidade_controller(
    nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
):
    nova_modalidade(nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo)


def editar_modalidade_controller(
    modalidade_id, nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
):
    editar_modalidade(
        modalidade_id, nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
    )


def excluir_modalidade_controller(modalidade_id):
    deletar_modalidade(modalidade_id)
