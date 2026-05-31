from database.db import get_connection


def listar_clientes_admin():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            u.id,
            u.nome,
            u.email,
            COALESCE(u.telefone, '') AS telefone,
            COALESCE(u.cpf, '') AS cpf,
            COALESCE(u.tipo, u.tipo_usuario, 'cliente') AS tipo,
            u.data_criacao,
            COUNT(p.id) AS total_pedidos,
            COALESCE(SUM(p.valor_total), 0) AS valor_total
        FROM usuarios u
        LEFT JOIN pedidos p ON p.usuario_id = u.id
        GROUP BY u.id
        ORDER BY u.data_criacao DESC NULLS LAST, u.id DESC
        """
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "nome": row[1],
            "email": row[2],
            "telefone": row[3],
            "cpf": row[4],
            "tipo": row[5],
            "data_criacao": row[6],
            "total_pedidos": int(row[7] or 0),
            "valor_total": float(row[8] or 0),
        }
        for row in rows
    ]
