from repositories.configuracao_repository import (
    obter_configuracoes,
    atualizar_configuracoes,
)


def buscar_configuracoes():
    return obter_configuracoes()


def salvar_configuracoes(
    nome_loja,
    slogan,
    email_contato,
    whatsapp,
    texto_rodape,
    cor_primaria,
    cor_secundaria,
    cidade_loja,
    estado_loja,
    cor_fundo,
    cor_fundo_secundario,
    cor_texto,
    cor_texto_secundario,
    logo_url,
):
    atualizar_configuracoes(
        nome_loja,
        slogan,
        email_contato,
        whatsapp,
        texto_rodape,
        cor_primaria,
        cor_secundaria,
        cidade_loja,
        estado_loja,
        cor_fundo,
        cor_fundo_secundario,
        cor_texto,
        cor_texto_secundario,
        logo_url,
    )
