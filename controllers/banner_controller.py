from services.banner_service import (
    banners_admin,
    banners_site,
    obter_banner,
    novo_banner,
    editar_banner,
    deletar_banner,
)


def listar_banners_admin_controller():
    return banners_admin()


def listar_banners_site_controller():
    return banners_site()


def obter_banner_controller(banner_id):
    return obter_banner(banner_id)


def criar_banner_controller(titulo, subtitulo, imagem_url, link, ativo, ordem):
    novo_banner(titulo, subtitulo, imagem_url, link, ativo, ordem)


def editar_banner_controller(
    banner_id, titulo, subtitulo, imagem_url, link, ativo, ordem
):
    editar_banner(banner_id, titulo, subtitulo, imagem_url, link, ativo, ordem)


def excluir_banner_controller(banner_id):
    deletar_banner(banner_id)
