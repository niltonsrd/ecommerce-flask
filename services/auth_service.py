import bcrypt
from repositories.usuario_repository import (
    criar_usuario,
    buscar_usuario_por_email,
    atualizar_usuario,
    atualizar_foto_usuario,
    buscar_usuario_por_id,
)


def registrar_usuario(nome, email, senha):
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
    criar_usuario(nome, email, senha_hash.decode())


def autenticar_usuario(email, senha):
    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return None

    senha_hash = usuario[3]

    if bcrypt.checkpw(senha.encode(), senha_hash.encode()):
        return usuario

    return None


def atualizar_usuario_service(usuario_id, nome, telefone, cpf, data_nascimento):
    if not nome or len(nome.strip()) < 3:
        raise ValueError("Informe um nome válido com pelo menos 3 caracteres.")

    atualizar_usuario(
        usuario_id,
        nome.strip(),
        telefone,
        cpf,
        data_nascimento
    )


def atualizar_foto_usuario_service(usuario_id, foto):
    atualizar_foto_usuario(usuario_id, foto)


def obter_usuario_por_id_service(usuario_id):
    return buscar_usuario_por_id(usuario_id)


def obter_usuario_por_email_service(email):
    return buscar_usuario_por_email(email)
