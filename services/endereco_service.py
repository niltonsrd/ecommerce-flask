from repositories import endereco_repository


def salvar_novo_endereco(usuario_id, dados):
    nome_destinatario = dados.get("nome_destinatario", "").strip()
    cep = dados.get("cep", "").strip()
    logradouro = dados.get("logradouro", "").strip()
    numero = dados.get("numero", "").strip()
    complemento = dados.get("complemento", "").strip()
    bairro = dados.get("bairro", "").strip()
    cidade = dados.get("cidade", "").strip()
    estado = dados.get("estado", "").strip().upper()
    referencia = dados.get("referencia", "").strip()
    principal = dados.get("principal") in ["true", "on", True, "1", 1]

    if not nome_destinatario:
        raise ValueError("Informe o nome do destinatário.")
    if not cep:
        raise ValueError("Informe o CEP.")
    if not logradouro:
        raise ValueError("Informe o logradouro.")
    if not numero:
        raise ValueError("Informe o número.")
    if not bairro:
        raise ValueError("Informe o bairro.")
    if not cidade:
        raise ValueError("Informe a cidade.")
    if not estado or len(estado) != 2:
        raise ValueError("Informe o estado com 2 letras.")

    return endereco_repository.criar_endereco(
        usuario_id=usuario_id,
        nome_destinatario=nome_destinatario,
        cep=cep,
        logradouro=logradouro,
        numero=numero,
        complemento=complemento,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        referencia=referencia,
        principal=principal,
    )


def listar_enderecos(usuario_id):
    return endereco_repository.listar_enderecos_usuario(usuario_id)


def buscar_endereco(endereco_id, usuario_id):
    return endereco_repository.buscar_endereco_por_id(endereco_id, usuario_id)


def buscar_endereco_principal(usuario_id):
    return endereco_repository.buscar_endereco_principal(usuario_id)


def tornar_endereco_principal(endereco_id, usuario_id):
    return endereco_repository.definir_endereco_principal(endereco_id, usuario_id)


def remover_endereco(endereco_id, usuario_id):
    return endereco_repository.excluir_endereco(endereco_id, usuario_id)
