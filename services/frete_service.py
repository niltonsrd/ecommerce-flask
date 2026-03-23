from repositories.frete_repository import (
    buscar_frete_por_cep,
    listar_fretes_admin,
    buscar_frete_admin,
    criar_frete_admin,
    atualizar_frete_admin,
    excluir_frete_admin,
)


def limpar_cep(cep):
    return "".join([c for c in cep if c.isdigit()])


def calcular_frete_por_cep(cep):

    cep_limpo = limpar_cep(cep)

    if len(cep_limpo) != 8:
        return None, "CEP inválido"

    frete = buscar_frete_por_cep(cep_limpo)

    if not frete:
        return None, "Não entregamos para esse CEP"

    return frete, None


def listar_fretes():
    return listar_fretes_admin()


def obter_frete(frete_id):
    return buscar_frete_admin(frete_id)


def novo_frete(nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo):
    criar_frete_admin(nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo)


def editar_frete(frete_id, nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo):
    atualizar_frete_admin(
        frete_id, nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo
    )


def deletar_frete(frete_id):
    excluir_frete_admin(frete_id)
