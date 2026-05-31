from database.db import get_connection


def listar_tamanhos():

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, nome FROM tamanhos ORDER BY nome"

    cursor.execute(query)

    tamanhos = cursor.fetchall()

    cursor.close()
    conn.close()

    return tamanhos


def salvar_estoque(produto_id, tamanho_id, quantidade):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO estoque (produto_id, tamanho_id, quantidade)
    VALUES (%s, %s, %s)
    ON CONFLICT (produto_id, tamanho_id)
    DO UPDATE SET
        quantidade = estoque.quantidade + EXCLUDED.quantidade,
        atualizado_em = NOW()
    RETURNING id;
    """

    cursor.execute(query, (produto_id, tamanho_id, quantidade))
    cursor.fetchone()

    cursor.execute(
        """
        INSERT INTO estoque_movimentacoes (
            produto_id, tamanho_id, tipo, quantidade, observacao
        )
        VALUES (%s, %s, 'REPOSICAO', %s, 'Ajuste manual pelo admin')
        """,
        (produto_id, tamanho_id, quantidade),
    )

    conn.commit()

    cursor.close()
    conn.close()


def verificar_estoque(produto_id, tamanho_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT GREATEST(quantidade - COALESCE(reservado, 0), 0)
    FROM estoque
    WHERE produto_id = %s
    AND tamanho_id = %s
    """

    cursor.execute(query, (produto_id, tamanho_id))

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado


def reduzir_estoque(produto_id, tamanho_id, quantidade):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE estoque
    SET quantidade = quantidade - %s
    WHERE produto_id = %s
    AND tamanho_id = %s
    """

    cursor.execute(query, (quantidade, produto_id, tamanho_id))

    conn.commit()

    cursor.close()
    conn.close()


def _movimentacao_existe(cursor, pedido_id, tipo):
    cursor.execute(
        """
        SELECT 1
        FROM estoque_movimentacoes
        WHERE pedido_id = %s
          AND tipo = %s
        LIMIT 1
        """,
        (pedido_id, tipo),
    )
    return cursor.fetchone() is not None


def confirmar_reserva_pedido(pedido_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if _movimentacao_existe(cursor, pedido_id, "BAIXA"):
            conn.rollback()
            return False

        cursor.execute(
            """
            SELECT produto_id, tamanho_id, quantidade
            FROM pedido_itens
            WHERE pedido_id = %s
            """,
            (pedido_id,),
        )
        itens = cursor.fetchall()

        for produto_id, tamanho_id, quantidade in itens:
            if not tamanho_id:
                continue

            cursor.execute(
                """
                SELECT quantidade, COALESCE(reservado, 0)
                FROM estoque
                WHERE produto_id = %s
                  AND tamanho_id = %s
                FOR UPDATE
                """,
                (produto_id, tamanho_id),
            )
            estoque = cursor.fetchone()
            if not estoque:
                raise ValueError("Estoque não encontrado para item do pedido.")

            quantidade_estoque = int(estoque[0] or 0)
            reservado = int(estoque[1] or 0)
            quantidade_item = int(quantidade)
            reserva_usada = min(reservado, quantidade_item)
            saldo_sem_reserva = quantidade_estoque - reservado
            baixa_sem_reserva = quantidade_item - reserva_usada

            if baixa_sem_reserva > saldo_sem_reserva:
                raise ValueError("Estoque insuficiente para baixa do pedido.")

            cursor.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade - %s,
                    reservado = reservado - %s,
                    atualizado_em = NOW()
                WHERE produto_id = %s
                  AND tamanho_id = %s
                """,
                (quantidade_item, reserva_usada, produto_id, tamanho_id),
            )
            cursor.execute(
                """
                INSERT INTO estoque_movimentacoes (
                    produto_id, tamanho_id, tipo, quantidade, pedido_id, observacao
                )
                VALUES (%s, %s, 'BAIXA', %s, %s, 'Baixa automática por pagamento aprovado')
                """,
                (produto_id, tamanho_id, quantidade, pedido_id),
            )

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def liberar_reserva_pedido(pedido_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if _movimentacao_existe(cursor, pedido_id, "BAIXA"):
            conn.rollback()
            return False
        if _movimentacao_existe(cursor, pedido_id, "LIBERACAO"):
            conn.rollback()
            return False

        cursor.execute(
            """
            SELECT produto_id, tamanho_id, quantidade
            FROM pedido_itens
            WHERE pedido_id = %s
            """,
            (pedido_id,),
        )
        itens = cursor.fetchall()

        for produto_id, tamanho_id, quantidade in itens:
            if not tamanho_id:
                continue

            cursor.execute(
                """
                SELECT COALESCE(reservado, 0)
                FROM estoque
                WHERE produto_id = %s
                  AND tamanho_id = %s
                FOR UPDATE
                """,
                (produto_id, tamanho_id),
            )
            row = cursor.fetchone()
            if not row:
                continue

            quantidade_liberada = min(int(row[0] or 0), int(quantidade))
            if quantidade_liberada <= 0:
                continue

            cursor.execute(
                """
                UPDATE estoque
                SET reservado = reservado - %s,
                    atualizado_em = NOW()
                WHERE produto_id = %s
                  AND tamanho_id = %s
                """,
                (quantidade_liberada, produto_id, tamanho_id),
            )
            cursor.execute(
                """
                INSERT INTO estoque_movimentacoes (
                    produto_id, tamanho_id, tipo, quantidade, pedido_id, observacao
                )
                VALUES (%s, %s, 'LIBERACAO', %s, %s, 'Reserva liberada por pedido cancelado/recusado')
                """,
                (produto_id, tamanho_id, quantidade_liberada, pedido_id),
            )

        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
