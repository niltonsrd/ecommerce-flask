from services.frete_service import (
    calcular_frete_por_cep,
    listar_fretes,
    obter_frete,
    novo_frete,
    editar_frete,
    deletar_frete,
)


def calcular_frete_controller(cep):
    return calcular_frete_por_cep(cep)


def listar_fretes_controller():
    return listar_fretes()


def obter_frete_controller(frete_id):
    return obter_frete(frete_id)


def criar_frete_controller(nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo):
    novo_frete(nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo)


def editar_frete_controller(
    frete_id, nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo
):
    editar_frete(frete_id, nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo)


def excluir_frete_controller(frete_id):
    deletar_frete(frete_id)
