from flask import render_template, request, redirect, session
from services.endereco_service import (
    salvar_novo_endereco,
    listar_enderecos,
    buscar_endereco_principal,
    tornar_endereco_principal,
    remover_endereco,
)


def listar_enderecos_controller():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    enderecos = listar_enderecos(usuario_id)
    endereco_principal = buscar_endereco_principal(usuario_id)

    return render_template(
        "loja/enderecos.html",
        enderecos=enderecos,
        endereco_principal=endereco_principal,
        pagina_conta="enderecos",
    )


def novo_endereco_controller():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    erro = None

    if request.method == "POST":
        try:
            salvar_novo_endereco(usuario_id, request.form)
            return redirect("/enderecos")
        except ValueError as e:
            erro = str(e)

    return render_template(
        "loja/novo_endereco.html",
        erro=erro,
        pagina_conta="enderecos",
    )


def definir_principal_controller(endereco_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    tornar_endereco_principal(endereco_id, usuario_id)
    return redirect("/enderecos")


def excluir_endereco_controller(endereco_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    remover_endereco(endereco_id, usuario_id)
    return redirect("/enderecos")
