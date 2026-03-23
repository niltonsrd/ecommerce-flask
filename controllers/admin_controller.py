from services.admin_service import (
    listar_produtos,
    novo_produto,
    remover_produto,
    obter_produto,
    editar_produto,
    imagens_produto,
    nova_imagem,
    deletar_imagem,
    imagem_principal,
)

from services.estoque_service import obter_tamanhos, adicionar_estoque
from services.categoria_service import (
    categorias,
    nova_categoria,
    obter_categoria,
    editar_categoria,
)
from services.pedido_service import pedidos_admin, mudar_status


def listar():
    return listar_produtos()


def criar(nome, descricao, preco, categoria_id, marca_id):
    return novo_produto(nome, descricao, preco, categoria_id, marca_id)


def deletar(produto_id):
    remover_produto(produto_id)


def produto(produto_id):
    return obter_produto(produto_id)


def editar(produto_id, nome, descricao, preco, categoria_id, marca_id, ativo):
    editar_produto(produto_id, nome, descricao, preco, categoria_id, marca_id, ativo)


def pedidos():
    return pedidos_admin()


def alterar_status(pedido_id, status):
    mudar_status(pedido_id, status)


def listar_categorias_admin():
    return categorias()


def criar_categoria_admin(nome, imagem_url=None):
    return nova_categoria(nome, imagem_url)


def obter_categoria_admin(categoria_id):
    return obter_categoria(categoria_id)


def editar_categoria_admin(categoria_id, nome, imagem_url=None):
    return editar_categoria(categoria_id, nome, imagem_url)


def tamanhos():
    return obter_tamanhos()


def estoque(produto_id, tamanho_id, quantidade):
    adicionar_estoque(produto_id, tamanho_id, quantidade)


def listar_imagens(produto_id):
    return imagens_produto(produto_id)


def adicionar_imagem(produto_id, imagem):
    nova_imagem(produto_id, imagem)


def excluir_imagem(imagem_id):
    deletar_imagem(imagem_id)


def definir_principal(produto_id, imagem_id):
    imagem_principal(produto_id, imagem_id)
