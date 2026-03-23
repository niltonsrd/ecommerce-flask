from services.home_bloco_service import (
    listar_blocos,
    listar_blocos_ativos,
    obter_bloco,
    criar_bloco,
    editar_bloco,
    excluir_bloco,
)


def listar_blocos_home_controller():
    return listar_blocos()


def listar_blocos_home_ativos_controller():
    return listar_blocos_ativos()


def obter_bloco_home_controller(bloco_id):
    return obter_bloco(bloco_id)


def criar_bloco_home_controller(
    nome,
    tipo_bloco,
    layout,
    titulo,
    subtitulo,
    descricao,
    imagem_url,
    texto_botao,
    link_botao,
    texto_botao_secundario,
    link_botao_secundario,
    cor_fundo,
    cor_texto,
    alinhamento_texto,
    ordem,
    ativo,
):
    criar_bloco(
        nome,
        tipo_bloco,
        layout,
        titulo,
        subtitulo,
        descricao,
        imagem_url,
        texto_botao,
        link_botao,
        texto_botao_secundario,
        link_botao_secundario,
        cor_fundo,
        cor_texto,
        alinhamento_texto,
        ordem,
        ativo,
    )


def editar_bloco_home_controller(
    bloco_id,
    nome,
    tipo_bloco,
    layout,
    titulo,
    subtitulo,
    descricao,
    imagem_url,
    texto_botao,
    link_botao,
    texto_botao_secundario,
    link_botao_secundario,
    cor_fundo,
    cor_texto,
    alinhamento_texto,
    ordem,
    ativo,
):
    editar_bloco(
        bloco_id,
        nome,
        tipo_bloco,
        layout,
        titulo,
        subtitulo,
        descricao,
        imagem_url,
        texto_botao,
        link_botao,
        texto_botao_secundario,
        link_botao_secundario,
        cor_fundo,
        cor_texto,
        alinhamento_texto,
        ordem,
        ativo,
    )


def excluir_bloco_home_controller(bloco_id):
    excluir_bloco(bloco_id)
