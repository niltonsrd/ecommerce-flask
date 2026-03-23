from flask import Blueprint, redirect, render_template, session, request, jsonify
from controllers.carrinho_controller import (
    adicionar_produto,
    ver_carrinho,
    remover_produto,
    obter_mini_carrinho,
    total_itens_carrinho,
)

carrinho_bp = Blueprint("carrinho", __name__)


@carrinho_bp.route("/adicionar-carrinho/<int:produto_id>")
def adicionar_carrinho(produto_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    tamanho_id = request.args.get("tamanho")
    quantidade = 1

    resultado = adicionar_produto(usuario_id, produto_id, tamanho_id, quantidade)

    if not resultado:
        return "Produto sem estoque disponível"

    return redirect("/carrinho")


@carrinho_bp.route("/carrinho/adicionar", methods=["POST"])
def adicionar_carrinho_post():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return (
            jsonify(
                {
                    "ok": False,
                    "redirect": "/login",
                    "message": "Faça login para adicionar ao carrinho.",
                }
            ),
            401,
        )

    produto_id = request.form.get("produto_id")
    tamanho_id = request.form.get("tamanho_id")
    quantidade = request.form.get("quantidade", 1)

    if not produto_id or not tamanho_id:
        return jsonify({"ok": False, "message": "Selecione o tamanho do produto."}), 400

    try:
        quantidade = int(quantidade)
    except ValueError:
        return jsonify({"ok": False, "message": "Quantidade inválida."}), 400

    if quantidade < 1:
        return jsonify({"ok": False, "message": "Quantidade inválida."}), 400

    resultado = adicionar_produto(usuario_id, produto_id, tamanho_id, quantidade)

    if not resultado:
        return jsonify({"ok": False, "message": "Produto sem estoque disponível."}), 400

    mini = obter_mini_carrinho(usuario_id)
    total_carrinho = total_itens_carrinho(usuario_id)

    return jsonify(
        {
            "ok": True,
            "message": "Produto adicionado ao carrinho.",
            "mini_carrinho": mini["itens"],
            "mini_carrinho_total": mini["total"],
            "total_carrinho": total_carrinho,
        }
    )


@carrinho_bp.route("/carrinho/mini")
def mini_carrinho_api():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify(
            {
                "ok": True,
                "mini_carrinho": [],
                "mini_carrinho_total": 0,
                "total_carrinho": 0,
            }
        )

    mini = obter_mini_carrinho(usuario_id)
    total_carrinho = total_itens_carrinho(usuario_id)

    return jsonify(
        {
            "ok": True,
            "mini_carrinho": mini["itens"],
            "mini_carrinho_total": mini["total"],
            "total_carrinho": total_carrinho,
        }
    )


@carrinho_bp.route("/carrinho/remover", methods=["POST"])
def remover_item_ajax():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return (
            jsonify(
                {
                    "ok": False,
                    "redirect": "/login",
                    "message": "Faça login para continuar.",
                }
            ),
            401,
        )

    item_id = request.form.get("item_id")

    if not item_id:
        return jsonify({"ok": False, "message": "Item inválido."}), 400

    remover_produto(item_id)

    mini = obter_mini_carrinho(usuario_id)
    total_carrinho = total_itens_carrinho(usuario_id)

    return jsonify(
        {
            "ok": True,
            "message": "Item removido do carrinho.",
            "mini_carrinho": mini["itens"],
            "mini_carrinho_total": mini["total"],
            "total_carrinho": total_carrinho,
        }
    )


@carrinho_bp.route("/carrinho", methods=["GET", "POST"])
def carrinho():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    itens = ver_carrinho(usuario_id)

    total = 0
    for item in itens:
        total += item[4] * item[5]

    return render_template(
        "loja/carrinho.html",
        itens=itens,
        total=total,
        pagina_conta="carrinho",
    )


@carrinho_bp.route("/remover-item/<int:item_id>")
def remover_item(item_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return redirect("/login")

    remover_produto(item_id)

    return redirect("/carrinho")
