from services.auth_service import (
    registrar_usuario,
    autenticar_usuario,
    atualizar_usuario_service,
    atualizar_foto_usuario_service,
    obter_usuario_por_id_service,
)


def cadastrar_usuario(nome, email, senha):
    registrar_usuario(nome, email, senha)


def login_usuario(email, senha):
    usuario = autenticar_usuario(email, senha)
    return usuario


def atualizar_dados_usuario(usuario_id, nome, telefone, cpf, data_nascimento):
    atualizar_usuario_service(usuario_id, nome, telefone, cpf, data_nascimento)


def atualizar_avatar_usuario(usuario_id, foto):
    atualizar_foto_usuario_service(usuario_id, foto)


def obter_usuario_por_id(usuario_id):
    return obter_usuario_por_id_service(usuario_id)
