from repositories.admin_repository import (
    listar_produtos_admin,
    criar_produto,
    deletar_produto,
    buscar_produto,
    atualizar_produto,
    listar_imagens_produto,
    adicionar_imagem_produto,
    remover_imagem_produto,
    definir_imagem_principal

)


def listar_produtos():
    return listar_produtos_admin()


def novo_produto(nome, descricao, preco, categoria_id, marca_id):
    return criar_produto(nome, descricao, preco, categoria_id, marca_id)


def remover_produto(produto_id):
    deletar_produto(produto_id)

def obter_produto(produto_id):
    return buscar_produto(produto_id)


def editar_produto(produto_id, nome, descricao, preco, categoria_id, marca_id, ativo):
    atualizar_produto(produto_id, nome, descricao, preco, categoria_id, marca_id, ativo)


def imagens_produto(produto_id):
    return listar_imagens_produto(produto_id)


def nova_imagem(produto_id, imagem):
    adicionar_imagem_produto(produto_id, imagem)


def deletar_imagem(imagem_id):
    remover_imagem_produto(imagem_id)


def imagem_principal(produto_id, imagem_id):
    definir_imagem_principal(produto_id, imagem_id)
