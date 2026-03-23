from database.db import get_connection


def criar_usuario(nome, email, senha):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO usuarios (nome, email, senha)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (nome, email, senha))

    conn.commit()

    cursor.close()
    conn.close()


def buscar_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM usuarios WHERE email = %s"

    cursor.execute(query, (email,))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario


def atualizar_usuario(usuario_id, nome):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE usuarios
    SET nome = %s
    WHERE id = %s
    """

    cursor.execute(query, (nome, usuario_id))
    conn.commit()

    cursor.close()
    conn.close()


def atualizar_foto_usuario(usuario_id, foto):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE usuarios
    SET foto = %s
    WHERE id = %s
    """

    cursor.execute(query, (foto, usuario_id))
    conn.commit()

    cursor.close()
    conn.close()


def buscar_usuario_por_id(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM usuarios
    WHERE id = %s
    """

    cursor.execute(query, (usuario_id,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario
