from database.db import get_connection


def criar_endereco(
    usuario_id,
    nome_destinatario,
    cep,
    logradouro,
    numero,
    complemento,
    bairro,
    cidade,
    estado,
    referencia,
    principal=False,
):
    conn = get_connection()
    cursor = conn.cursor()

    if principal:
        cursor.execute(
            "UPDATE enderecos SET principal = FALSE WHERE usuario_id = %s",
            (usuario_id,),
        )

    query = """
        INSERT INTO enderecos (
            usuario_id, nome_destinatario, cep, logradouro, numero,
            complemento, bairro, cidade, estado, referencia, principal
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """

    cursor.execute(
        query,
        (
            usuario_id,
            nome_destinatario,
            cep,
            logradouro,
            numero,
            complemento,
            bairro,
            cidade,
            estado,
            referencia,
            principal,
        ),
    )

    endereco_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return endereco_id


def buscar_endereco_por_id(endereco_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, usuario_id, nome_destinatario, cep, logradouro, numero,
               complemento, bairro, cidade, estado, referencia, principal
        FROM enderecos
        WHERE id = %s AND usuario_id = %s
    """
    cursor.execute(query, (endereco_id, usuario_id))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "usuario_id": row[1],
        "nome_destinatario": row[2],
        "cep": row[3],
        "logradouro": row[4],
        "numero": row[5],
        "complemento": row[6],
        "bairro": row[7],
        "cidade": row[8],
        "estado": row[9],
        "referencia": row[10],
        "principal": row[11],
    }


def listar_enderecos_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, nome_destinatario, cep, logradouro, numero,
               complemento, bairro, cidade, estado, referencia, principal
        FROM enderecos
        WHERE usuario_id = %s
        ORDER BY principal DESC, id DESC
    """
    cursor.execute(query, (usuario_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    enderecos = []
    for row in rows:
        enderecos.append(
            {
                "id": row[0],
                "nome_destinatario": row[1],
                "cep": row[2],
                "logradouro": row[3],
                "numero": row[4],
                "complemento": row[5],
                "bairro": row[6],
                "cidade": row[7],
                "estado": row[8],
                "referencia": row[9],
                "principal": row[10],
            }
        )

    return enderecos


def buscar_endereco_principal(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT id, nome_destinatario, cep, logradouro, numero,
               complemento, bairro, cidade, estado, referencia, principal
        FROM enderecos
        WHERE usuario_id = %s AND principal = TRUE
        LIMIT 1
    """
    cursor.execute(query, (usuario_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "nome_destinatario": row[1],
        "cep": row[2],
        "logradouro": row[3],
        "numero": row[4],
        "complemento": row[5],
        "bairro": row[6],
        "cidade": row[7],
        "estado": row[8],
        "referencia": row[9],
        "principal": row[10],
    }


def definir_endereco_principal(endereco_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE enderecos SET principal = FALSE WHERE usuario_id = %s",
        (usuario_id,),
    )

    cursor.execute(
        "UPDATE enderecos SET principal = TRUE WHERE id = %s AND usuario_id = %s",
        (endereco_id, usuario_id),
    )

    conn.commit()

    cursor.close()
    conn.close()


def excluir_endereco(endereco_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM enderecos WHERE id = %s AND usuario_id = %s",
        (endereco_id, usuario_id),
    )

    conn.commit()

    cursor.close()
    conn.close()
