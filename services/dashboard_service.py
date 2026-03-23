from repositories.dashboard_repository import (
    buscar_faturamento_total,
    buscar_faturamento_hoje,
    buscar_pedidos_hoje,
    buscar_clientes_novos_hoje,
    buscar_produtos_mais_vendidos,
    buscar_estoque_baixo,
)


def obter_dados_dashboard():
    return {
        "faturamento_total": buscar_faturamento_total(),
        "faturamento_hoje": buscar_faturamento_hoje(),
        "pedidos_hoje": buscar_pedidos_hoje(),
        "clientes_novos_hoje": buscar_clientes_novos_hoje(),
        "produtos_mais_vendidos": buscar_produtos_mais_vendidos(),
        "estoque_baixo": buscar_estoque_baixo(),
    }
