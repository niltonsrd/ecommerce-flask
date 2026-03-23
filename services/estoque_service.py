from repositories.estoque_repository import (listar_tamanhos, 
salvar_estoque,
verificar_estoque,
reduzir_estoque
)


def obter_tamanhos():

    return listar_tamanhos()


def adicionar_estoque(produto_id, tamanho_id, quantidade):

    salvar_estoque(produto_id, tamanho_id, quantidade)


def estoque_disponivel(produto_id, tamanho_id):

    estoque = verificar_estoque(produto_id, tamanho_id)

    if estoque and estoque[0] > 0:
        return True

    return False


def diminuir_estoque(produto_id, tamanho_id, quantidade):

    reduzir_estoque(produto_id, tamanho_id, quantidade)
