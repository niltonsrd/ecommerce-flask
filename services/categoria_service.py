from repositories.categoria_repository import (
    listar_categorias,
    criar_categoria,
    buscar_categoria_por_id,
    atualizar_categoria,
)


def categorias():
    return listar_categorias()


def nova_categoria(nome, imagem_url=None):
    criar_categoria(nome, imagem_url)


def obter_categoria(categoria_id):
    return buscar_categoria_por_id(categoria_id)


def editar_categoria(categoria_id, nome, imagem_url=None):
    atualizar_categoria(categoria_id, nome, imagem_url)
