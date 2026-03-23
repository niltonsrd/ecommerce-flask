from repositories.banner_repository import (
    listar_banners_admin,
    listar_banners_ativos,
    buscar_banner_por_id,
    criar_banner,
    atualizar_banner,
    excluir_banner,
)


def banners_admin():
    return listar_banners_admin()


def banners_site():
    return listar_banners_ativos()


def obter_banner(banner_id):
    return buscar_banner_por_id(banner_id)


def novo_banner(titulo, subtitulo, imagem_url, link, ativo, ordem):
    criar_banner(titulo, subtitulo, imagem_url, link, ativo, ordem)


def editar_banner(banner_id, titulo, subtitulo, imagem_url, link, ativo, ordem):
    atualizar_banner(banner_id, titulo, subtitulo, imagem_url, link, ativo, ordem)


def deletar_banner(banner_id):
    excluir_banner(banner_id)
