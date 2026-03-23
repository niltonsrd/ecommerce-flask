from repositories import checkout_repository
from services import endereco_service, pagamento_service
from controllers.configuracao_controller import obter_configuracoes_controller


def calcular_desconto(cupom, subtotal):
    if not cupom:
        return 0.0

    if not cupom["ativo"]:
        raise ValueError("Cupom inválido ou inativo.")

    valor_minimo = float(cupom.get("valor_minimo") or 0)
    if subtotal < valor_minimo:
        raise ValueError(f"Esse cupom exige compra mínima de R$ {valor_minimo:.2f}.")

    tipo = (cupom.get("tipo_desconto") or "").upper()
    valor = float(cupom.get("valor_desconto") or 0)

    if tipo in ["PERCENTUAL", "PORCENTAGEM"]:
        desconto = subtotal * (valor / 100)
    elif tipo in ["FIXO", "VALOR_FIXO"]:
        desconto = valor
    else:
        desconto = 0.0

    if desconto > subtotal:
        desconto = subtotal

    return round(desconto, 2)


def validar_estoque(itens):
    if not itens:
        raise ValueError("Seu carrinho está vazio.")

    for item in itens:
        if item["quantidade"] > item["estoque_disponivel"]:
            raise ValueError(
                f"Estoque insuficiente para o produto {item['nome']} no tamanho {item['tamanho_nome']}."
            )


def montar_checkout(usuario_id):
    itens = checkout_repository.buscar_itens_carrinho(usuario_id)
    enderecos = endereco_service.listar_enderecos(usuario_id)
    modalidades = checkout_repository.listar_modalidades_ativas()

    config = obter_configuracoes_controller()

    cidade_loja = ""
    estado_loja = ""

    if config:
        if len(config) > 8 and config[8]:
            cidade_loja = str(config[8]).strip()
        if len(config) > 9 and config[9]:
            estado_loja = str(config[9]).strip()

    subtotal = round(sum(item["subtotal"] for item in itens), 2)

    return {
        "itens": itens,
        "enderecos": enderecos,
        "modalidades": modalidades,
        "subtotal": subtotal,
        "desconto": 0.0,
        "frete": 0.0,
        "total": subtotal,
        "cupom_aplicado": None,
        "cupom_codigo": "",
        "modalidade_escolhida": None,
        "cidade_loja": cidade_loja,
        "estado_loja": estado_loja,
    }


def validar_cupom_checkout(usuario_id, codigo):
    itens = checkout_repository.buscar_itens_carrinho(usuario_id)
    subtotal = round(sum(item["subtotal"] for item in itens), 2)

    if not codigo:
        raise ValueError("Informe um cupom.")

    cupom = checkout_repository.buscar_cupom_por_codigo(codigo.strip())

    if not cupom:
        raise ValueError("Cupom não encontrado.")

    desconto = calcular_desconto(cupom, subtotal)
    total_com_desconto = round(subtotal - desconto, 2)

    if total_com_desconto < 0:
        total_com_desconto = 0.0

    return {
        "codigo": cupom["codigo"],
        "desconto": desconto,
        "subtotal": subtotal,
        "total_com_desconto": total_com_desconto,
    }


def processar_checkout(usuario_id, form_data):
    itens = checkout_repository.buscar_itens_carrinho(usuario_id)
    validar_estoque(itens)

    subtotal = round(sum(item["subtotal"] for item in itens), 2)

    endereco_id = form_data.get("endereco_id")
    usar_novo_endereco = form_data.get("usar_novo_endereco")
    modalidade_entrega_id = form_data.get("modalidade_entrega_id")
    cupom_codigo = (form_data.get("cupom_codigo") or "").strip()
    forma_pagamento = (form_data.get("forma_pagamento") or "").strip().upper()
    observacoes = (form_data.get("observacoes") or "").strip()

    if not modalidade_entrega_id:
        raise ValueError("Selecione a modalidade de entrega.")

    modalidade = checkout_repository.buscar_modalidade_entrega_por_id(
        int(modalidade_entrega_id)
    )
    if not modalidade:
        raise ValueError("Modalidade de entrega inválida.")

    if forma_pagamento not in ["PIX", "CARTAO", "BOLETO"]:
        raise ValueError("Selecione uma forma de pagamento válida.")

    tipo_modalidade = (modalidade.get("tipo") or "").upper()
    exige_endereco = tipo_modalidade != "RETIRADA"

    endereco_id_final = None

    if exige_endereco:
        if usar_novo_endereco == "1":
            novo_endereco_id = endereco_service.salvar_novo_endereco(
                usuario_id, form_data
            )
            endereco_id_final = novo_endereco_id
        else:
            if not endereco_id:
                raise ValueError("Selecione um endereço ou cadastre um novo.")
            endereco = endereco_service.buscar_endereco(int(endereco_id), usuario_id)
            if not endereco:
                raise ValueError("Endereço inválido.")
            endereco_id_final = endereco["id"]

    cupom = None
    desconto = 0.0
    cupom_id = None

    if cupom_codigo:
        cupom = checkout_repository.buscar_cupom_por_codigo(cupom_codigo)
        if not cupom:
            raise ValueError("Cupom não encontrado.")
        desconto = calcular_desconto(cupom, subtotal)
        cupom_id = cupom["id"]

    valor_frete = round(float(modalidade["valor"]), 2)

    if tipo_modalidade == "RETIRADA":
        valor_frete = 0.0

    valor_total = round(subtotal - desconto + valor_frete, 2)

    if valor_total < 0:
        valor_total = 0.0

    pedido_id = checkout_repository.criar_pedido(
        usuario_id=usuario_id,
        endereco_id=endereco_id_final,
        cupom_id=cupom_id,
        subtotal=subtotal,
        desconto=desconto,
        valor_frete=valor_frete,
        valor_total=valor_total,
        modalidade_entrega_id=modalidade["id"],
        prazo_entrega=modalidade["prazo"],
        forma_pagamento=forma_pagamento,
        observacoes=observacoes,
    )

    for item in itens:
        checkout_repository.adicionar_item_pedido(
            pedido_id=pedido_id,
            produto_id=item["produto_id"],
            tamanho_id=item["tamanho_id"],
            quantidade=item["quantidade"],
            preco=item["preco"],
        )

    pagamento = pagamento_service.criar_pagamento_inicial(
        pedido_id=pedido_id, metodo=forma_pagamento, valor=valor_total
    )

    checkout_repository.limpar_carrinho_usuario(usuario_id)

    pedido = checkout_repository.buscar_pedido_por_id(pedido_id, usuario_id)

    return {"pedido": pedido, "pagamento": pagamento}
