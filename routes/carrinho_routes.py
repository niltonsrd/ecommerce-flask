from flask import Blueprint, jsonify, redirect, render_template, request, session

from controllers.carrinho_controller import (
    adicionar_produto,
    adicionar_produto_anonimo,
    atualizar_quantidade_produto,
    atualizar_quantidade_produto_anonimo,
    limpar_carrinho,
    limpar_carrinho_anonimo,
    obter_mini_carrinho,
    obter_mini_carrinho_anonimo,
    remover_produto,
    remover_produto_anonimo,
    total_itens_carrinho,
    total_itens_carrinho_anonimo,
    ver_carrinho,
    ver_carrinho_anonimo,
)
from services.carrinho_service import SESSION_CART_KEY

carrinho_bp = Blueprint("carrinho", __name__)


def _carrinho_sessao():
    return session.get(SESSION_CART_KEY, {})


def _wants_json():
    return request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _salvar_carrinho_sessao(carrinho):
    session[SESSION_CART_KEY] = carrinho
    session.modified = True


def _payload_carrinho(usuario_id=None):
    if usuario_id:
        mini = obter_mini_carrinho(usuario_id)
        total_carrinho = total_itens_carrinho(usuario_id)
    else:
        carrinho = _carrinho_sessao()
        mini = obter_mini_carrinho_anonimo(carrinho)
        total_carrinho = total_itens_carrinho_anonimo(carrinho)

    return {
        "mini_carrinho": mini["itens"],
        "mini_carrinho_total": mini["total"],
        "total_carrinho": total_carrinho,
    }


def _json_carrinho(ok=True, message=None, status=200):
    payload = {"ok": ok}
    if message:
        payload["message"] = message
    payload.update(_payload_carrinho(session.get("usuario_id")))
    return jsonify(payload), status


def _atualizar_quantidade_item(item_id, quantidade):
    usuario_id = session.get("usuario_id")

    if usuario_id:
        ok = atualizar_quantidade_produto(usuario_id, item_id, quantidade)
    else:
        ok, carrinho = atualizar_quantidade_produto_anonimo(
            _carrinho_sessao(), item_id, quantidade
        )
        _salvar_carrinho_sessao(carrinho)

    return ok


@carrinho_bp.route("/carrinho/adicionar", methods=["POST"])
def adicionar_carrinho_post():
    usuario_id = session.get("usuario_id")
    produto_id = request.form.get("produto_id")
    tamanho_id = request.form.get("tamanho_id") or request.form.get("tamanho")
    quantidade = request.form.get("quantidade", 1)

    if not produto_id or not tamanho_id:
        return jsonify({"ok": False, "message": "Selecione o tamanho do produto."}), 400

    try:
        quantidade = int(quantidade)
    except ValueError:
        return jsonify({"ok": False, "message": "Quantidade inválida."}), 400

    if quantidade < 1:
        return jsonify({"ok": False, "message": "Quantidade inválida."}), 400

    if usuario_id:
        resultado = adicionar_produto(usuario_id, produto_id, tamanho_id, quantidade)
        if not resultado:
            return jsonify({"ok": False, "message": "Estoque insuficiente para a quantidade selecionada."}), 400
    else:
        resultado, carrinho = adicionar_produto_anonimo(
            _carrinho_sessao(), produto_id, tamanho_id, quantidade
        )
        if not resultado:
            return jsonify({"ok": False, "message": "Estoque insuficiente para a quantidade selecionada."}), 400
        _salvar_carrinho_sessao(carrinho)

    if not _wants_json():
        return redirect("/carrinho")
    return _json_carrinho(True, "Produto adicionado ao carrinho.")


@carrinho_bp.route("/carrinho/mini")
def mini_carrinho_api():
    payload = {"ok": True}
    payload.update(_payload_carrinho(session.get("usuario_id")))
    return jsonify(payload)


@carrinho_bp.route("/carrinho/remover", methods=["POST"])
def remover_item_ajax():
    usuario_id = session.get("usuario_id")
    item_id = request.form.get("item_id")

    if not item_id:
        return jsonify({"ok": False, "message": "Item inválido."}), 400

    if usuario_id:
        remover_produto(item_id, usuario_id)
    else:
        _salvar_carrinho_sessao(remover_produto_anonimo(_carrinho_sessao(), item_id))

    if not _wants_json():
        return redirect("/carrinho")
    return _json_carrinho(True, "Item removido do carrinho.")


@carrinho_bp.route("/carrinho/quantidade", methods=["POST"])
def atualizar_quantidade_item_ajax():
    usuario_id = session.get("usuario_id")
    item_id = request.form.get("item_id")
    quantidade = request.form.get("quantidade")

    if not item_id or quantidade is None:
        return jsonify({"ok": False, "message": "Item inválido."}), 400

    try:
        quantidade = int(quantidade)
    except ValueError:
        return jsonify({"ok": False, "message": "Quantidade inválida."}), 400

    ok = _atualizar_quantidade_item(item_id, quantidade)

    if not ok:
        return jsonify({"ok": False, "message": "Estoque insuficiente para a quantidade selecionada."}), 400

    if not _wants_json():
        return redirect("/carrinho")
    return _json_carrinho(True, "Quantidade atualizada.")


@carrinho_bp.route("/carrinho/incrementar", methods=["POST"])
def incrementar_item_ajax():
    item_id = request.form.get("item_id")
    quantidade_atual = request.form.get("quantidade_atual", 0)

    if not item_id:
        return jsonify({"ok": False, "message": "Item inválido."}), 400

    try:
        nova_quantidade = int(quantidade_atual) + 1
    except ValueError:
        return jsonify({"ok": False, "message": "Quantidade inválida."}), 400

    if not _atualizar_quantidade_item(item_id, nova_quantidade):
        return jsonify({"ok": False, "message": "Estoque insuficiente para a quantidade selecionada."}), 400

    return _json_carrinho(True, "Quantidade atualizada.")


@carrinho_bp.route("/carrinho/decrementar", methods=["POST"])
def decrementar_item_ajax():
    item_id = request.form.get("item_id")
    quantidade_atual = request.form.get("quantidade_atual", 0)

    if not item_id:
        return jsonify({"ok": False, "message": "Item inválido."}), 400

    try:
        nova_quantidade = max(int(quantidade_atual) - 1, 0)
    except ValueError:
        return jsonify({"ok": False, "message": "Quantidade inválida."}), 400

    if not _atualizar_quantidade_item(item_id, nova_quantidade):
        return jsonify({"ok": False, "message": "Não foi possível atualizar o item."}), 400

    return _json_carrinho(True, "Quantidade atualizada.")


@carrinho_bp.route("/carrinho/limpar", methods=["POST"])
def limpar_carrinho_route():
    usuario_id = session.get("usuario_id")
    if usuario_id:
        limpar_carrinho(usuario_id)
    else:
        _salvar_carrinho_sessao(limpar_carrinho_anonimo())

    return redirect("/carrinho")


@carrinho_bp.route("/carrinho", methods=["GET", "POST"])
def carrinho():
    usuario_id = session.get("usuario_id")
    if usuario_id:
        itens = ver_carrinho(usuario_id)
    else:
        itens = ver_carrinho_anonimo(_carrinho_sessao())

    total = sum(float(item["preco"]) * int(item["quantidade"]) for item in itens)
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
        return redirect("/carrinho")
    remover_produto(item_id, usuario_id)
    return redirect("/carrinho")
