from repositories.cupom_admin_repository import (
    listar_cupons_admin,
    buscar_cupom_admin,
    criar_cupom_admin,
    atualizar_cupom_admin,
    excluir_cupom_admin,
)


def listar_cupons():
    return listar_cupons_admin()


def obter_cupom(cupom_id):
    return buscar_cupom_admin(cupom_id)


def novo_cupom(
    codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim
):
    criar_cupom_admin(
        codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim
    )


def editar_cupom(
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
    atualizar_cupom_admin(
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


def deletar_cupom(cupom_id):
    excluir_cupom_admin(cupom_id)
