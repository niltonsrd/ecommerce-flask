from services.cupom_admin_service import (
    listar_cupons,
    obter_cupom,
    novo_cupom,
    editar_cupom,
    deletar_cupom,
)


def listar_cupons_controller():
    return listar_cupons()


def obter_cupom_controller(cupom_id):
    return obter_cupom(cupom_id)


def criar_cupom_controller(
    codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim
):
    novo_cupom(
        codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim
    )


def editar_cupom_controller(
    cupom_id,
    codigo,
    tipo,
    valor,
    valor_minimo,
    limite_uso,
    ativo,
    data_inicio,
    data_fim,
):
    editar_cupom(
        cupom_id,
        codigo,
        tipo,
        valor,
        valor_minimo,
        limite_uso,
        ativo,
        data_inicio,
        data_fim,
    )


def excluir_cupom_controller(cupom_id):
    deletar_cupom(cupom_id)
