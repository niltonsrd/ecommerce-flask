from services.configuracao_service import buscar_configuracoes, salvar_configuracoes


def obter_configuracoes_controller():
    return buscar_configuracoes()


def salvar_configuracoes_controller(
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
    salvar_configuracoes(
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
