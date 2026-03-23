from repositories.home_bloco_repository import (
    listar_blocos_home,
    listar_blocos_home_ativos,
    obter_bloco_home_por_id,
    criar_bloco_home,
    editar_bloco_home,
    excluir_bloco_home,
)


def listar_blocos():
    return listar_blocos_home()


def listar_blocos_ativos():
    return listar_blocos_home_ativos()


def obter_bloco(bloco_id):
    return obter_bloco_home_por_id(bloco_id)


def criar_bloco(
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
    criar_bloco_home(
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


def editar_bloco(
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
    editar_bloco_home(
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


def excluir_bloco(bloco_id):
    excluir_bloco_home(bloco_id)
