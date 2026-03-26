from repositories.dashboard_repository import (
    buscar_faturamento_total,
    buscar_faturamento_hoje,
    buscar_faturamento_mes,
    buscar_pedidos_hoje,
    buscar_pedidos_pendentes,
    buscar_clientes_novos_hoje,
    buscar_ticket_medio,
    buscar_total_estoque_critico,
    buscar_produtos_mais_vendidos,
    buscar_estoque_baixo,
    buscar_status_pedidos,
    buscar_expedicao,
    buscar_pedidos_recentes,
    buscar_clientes_recentes,
)


def formatar_data(data):
    if not data:
        return ""
    return data.strftime("%d/%m/%Y %H:%M")


def limpar_telefone_whatsapp(telefone):
    if not telefone:
        return ""

    numeros = "".join(filter(str.isdigit, str(telefone)))

    if not numeros:
        return ""

    if numeros.startswith("55"):
        return numeros

    return f"55{numeros}"


def obter_dados_dashboard():
    pedidos_recentes = buscar_pedidos_recentes()
    clientes_recentes = buscar_clientes_recentes()

    for pedido in pedidos_recentes:
        pedido["data_formatada"] = formatar_data(pedido.get("data_pedido"))
        pedido["whatsapp_link"] = limpar_telefone_whatsapp(
            pedido.get("cliente_telefone")
        )

    for cliente in clientes_recentes:
        cliente["data_formatada"] = formatar_data(cliente.get("data_criacao"))
        cliente["whatsapp_link"] = limpar_telefone_whatsapp(cliente.get("telefone"))

    return {
        "faturamento_total": buscar_faturamento_total(),
        "faturamento_hoje": buscar_faturamento_hoje(),
        "faturamento_mes": buscar_faturamento_mes(),
        "pedidos_hoje": buscar_pedidos_hoje(),
        "pedidos_pendentes": buscar_pedidos_pendentes(),
        "clientes_novos_hoje": buscar_clientes_novos_hoje(),
        "ticket_medio": buscar_ticket_medio(),
        "total_estoque_critico": buscar_total_estoque_critico(),
        "produtos_mais_vendidos": buscar_produtos_mais_vendidos(),
        "estoque_baixo": buscar_estoque_baixo(),
        "status_pedidos": buscar_status_pedidos(),
        "expedicao": buscar_expedicao(),
        "pedidos_recentes": pedidos_recentes,
        "clientes_recentes": clientes_recentes,
    }
