from flask import render_template, request, redirect, url_for, session, flash, jsonify
from services import checkout_service, endereco_service
from services.pix_service import gerar_dados_pix
from services.pagamento_service import enviar_comprovante_pagamento


def exibir_checkout():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        flash("Faça login para continuar.", "erro")
        return redirect(url_for("auth.login"))

    dados = checkout_service.montar_checkout(usuario_id)

    if not dados["itens"]:
        flash("Seu carrinho está vazio.", "erro")
        return redirect(url_for("carrinho.carrinho"))

    return render_template("checkout.html", **dados)


def finalizar_checkout():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        flash("Faça login para continuar.", "erro")
        return redirect(url_for("auth.login"))

    try:
        resultado = checkout_service.processar_checkout(usuario_id, request.form)
        pedido = resultado["pedido"]

        forma_pagamento = str(request.form.get("forma_pagamento") or "").strip().upper()

        if forma_pagamento == "PIX":
            return redirect(
                url_for("checkout.exibir_pagamento_checkout", pedido_id=pedido["id"])
            )

        return redirect(url_for("checkout.checkout_sucesso", pedido_id=pedido["id"]))

    except Exception as e:
        flash(str(e), "erro")
        return redirect(url_for("checkout.exibir_checkout"))


def exibir_pagamento_checkout(pedido_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        flash("Faça login para continuar.", "erro")
        return redirect(url_for("auth.login"))

    from repositories import checkout_repository, pagamento_repository

    pedido = checkout_repository.buscar_pedido_por_id(pedido_id, usuario_id)

    if not pedido:
        flash("Pedido não encontrado.", "erro")
        return redirect("/")

    pagamento = pagamento_repository.buscar_pagamento_por_pedido(pedido_id)

    if not pagamento:
        pagamento = {
            "pedido_id": pedido["id"],
            "valor": float(pedido["valor_total"]),
            "status": "PENDENTE",
            "metodo": pedido.get("forma_pagamento", "PIX"),
            "gateway": "MANUAL",
            "detalhes": "Faça o PIX e envie o comprovante para confirmação manual.",
        }

    pix = gerar_dados_pix(valor=float(pagamento["valor"]), pedido_id=int(pedido["id"]))

    return render_template(
        "checkout_pix_manual.html",
        pedido=pedido,
        pagamento=pagamento,
        chave_pix_loja=pix["chave_pix"],
        pix_payload=pix["payload_pix"],
        qr_code_base64=pix["qr_code_base64"],
        pix_recebedor=pix["recebedor"],
        pix_cidade=pix["cidade"],
        pix_banco=pix["banco"],
        pix_tipo_chave=pix["tipo_chave"],
    )


def checkout_sucesso(pedido_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        flash("Faça login para continuar.", "erro")
        return redirect(url_for("auth.login"))

    from repositories import (
        checkout_repository,
        pagamento_repository,
        endereco_repository,
    )

    pedido = checkout_repository.buscar_pedido_por_id(pedido_id, usuario_id)

    if not pedido:
        flash("Pedido não encontrado.", "erro")
        return redirect("/")

    pagamento = pagamento_repository.buscar_pagamento_por_pedido(pedido_id)
    endereco = None

    if pedido["endereco_id"]:
        endereco = endereco_repository.buscar_endereco_por_id(
            pedido["endereco_id"], usuario_id
        )

    return render_template(
        "checkout_sucesso.html", pedido=pedido, pagamento=pagamento, endereco=endereco
    )


def validar_cupom_ajax():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({"sucesso": False, "erro": "Faça login para continuar."}), 401

    try:
        codigo = (request.form.get("cupom_codigo") or "").strip()
        resultado = checkout_service.validar_cupom_checkout(usuario_id, codigo)
        return jsonify({"sucesso": True, "dados": resultado})
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


def salvar_endereco_ajax():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({"sucesso": False, "erro": "Faça login para continuar."}), 401

    try:
        endereco_id = endereco_service.salvar_novo_endereco(usuario_id, request.form)
        endereco = endereco_service.buscar_endereco(endereco_id, usuario_id)

        return jsonify({"sucesso": True, "endereco": endereco})
    except Exception as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


def enviar_comprovante_checkout(pedido_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        flash("Faça login para continuar.", "erro")
        return redirect(url_for("auth.login"))

    from repositories import checkout_repository, pagamento_repository

    pedido = checkout_repository.buscar_pedido_por_id(pedido_id, usuario_id)

    if not pedido:
        flash("Pedido não encontrado.", "erro")
        return redirect("/")

    arquivo = request.files.get("comprovante")
    observacao = (request.form.get("observacao_cliente") or "").strip()

    try:
        enviar_comprovante_pagamento(
            pedido_id=pedido_id, arquivo=arquivo, observacao_cliente=observacao
        )
        flash(
            "Comprovante enviado com sucesso. Aguarde a confirmação do pagamento.",
            "sucesso",
        )
    except Exception as e:
        flash(str(e), "erro")

    return redirect(url_for("checkout.exibir_pagamento_checkout", pedido_id=pedido_id))
