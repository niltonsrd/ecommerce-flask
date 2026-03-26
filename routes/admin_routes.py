from werkzeug.utils import secure_filename
import os
from flask import Blueprint, render_template, request, redirect, current_app, session
from repositories.admin_repository import salvar_imagem
from controllers.admin_controller import ( listar, 
    criar, 
    deletar, 
    produto, 
    editar, 
    pedidos, 
    alterar_status,
    listar_categorias_admin,
    criar_categoria_admin,
    tamanhos,
    estoque,
    listar_imagens,
    adicionar_imagem,
    excluir_imagem,
    definir_principal,
    obter_categoria_admin,
    editar_categoria_admin
)
from services.marca_service import marcas
from controllers.configuracao_controller import (obter_configuracoes_controller,
    salvar_configuracoes_controller
)
from controllers.admin_dashboard_controller import dashboard_admin
from controllers.cupom_admin_controller import (
    listar_cupons_controller,
    obter_cupom_controller,
    criar_cupom_controller,
    editar_cupom_controller,
    excluir_cupom_controller,
)
from controllers.banner_controller import (
    listar_banners_admin_controller,
    obter_banner_controller,
    criar_banner_controller,
    editar_banner_controller,
    excluir_banner_controller,
)
from controllers.frete_controller import (
    listar_fretes_controller,
    obter_frete_controller,
    criar_frete_controller,
    editar_frete_controller,
    excluir_frete_controller
)
from controllers.modalidade_entrega_controller import (
    listar_modalidades_controller,
    obter_modalidade_controller,
    criar_modalidade_controller,
    editar_modalidade_controller,
    excluir_modalidade_controller,
)
from controllers.home_bloco_controller import (
    listar_blocos_home_controller,
    obter_bloco_home_controller,
    criar_bloco_home_controller,
    editar_bloco_home_controller,
    excluir_bloco_home_controller,
)
from repositories.pagamento_repository import buscar_pagamento_por_pedido, atualizar_status_pagamento
from repositories.pedido_repository import (
    atualizar_status as atualizar_status_pedido_db,
)
from controllers.pedido_controller import ver_detalhe_pedido_admin


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def usuario_logado():
    return session.get("usuario_id") is not None


def admin_logado():
    return session.get("usuario_tipo") == "admin"


@admin_bp.route("/")
def dashboard():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    dados_dashboard = dashboard_admin()

    return render_template("admin/dashboard.html", dashboard=dados_dashboard)


@admin_bp.route("/produtos")
def produtos():

    if not usuario_logado():
        return redirect("/login")
    
    if not admin_logado():
        return redirect("/produtos")
    

    produtos = listar()

    return render_template("admin/produtos.html", produtos=produtos)


@admin_bp.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():

    if not usuario_logado():
        return redirect("/login")
    
    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        categoria_id = request.form["categoria"]
        marca_id = request.form["marca"]

        imagem = request.files["imagem"]

        nome_arquivo = None

        if imagem:
            nome_arquivo = secure_filename(imagem.filename)

            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)

            imagem.save(caminho)

        produto_id = criar(nome, descricao, preco, categoria_id, marca_id)

        if nome_arquivo:
            salvar_imagem(produto_id, nome_arquivo)

        return redirect("/admin/produtos")

    categorias = listar_categorias_admin()
    lista_marcas = marcas()

    return render_template(
        "admin/novo_produto.html", categorias=categorias, marcas=lista_marcas
    )


@admin_bp.route("/produtos/deletar/<int:id>")
def deletar_produto(id):
    
    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    deletar(id)

    return redirect("/admin/produtos")


@admin_bp.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
def editar_produto_page(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        nome = request.form["nome"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        categoria_id = request.form["categoria"]
        marca_id = request.form["marca"]
        ativo = request.form["ativo"] == "true"

        editar(id, nome, descricao, preco, categoria_id, marca_id, ativo)

        return redirect("/admin/produtos")

    produto_dados = produto(id)
    categorias = listar_categorias_admin()
    lista_marcas = marcas()

    return render_template(
        "admin/editar_produto.html",
        produto=produto_dados,
        categorias=categorias,
        marcas=lista_marcas,
    )


@admin_bp.route("/pedidos")
def pedidos_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    lista = pedidos()

    return render_template("admin/pedidos.html", pedidos=lista, buscar_pagamento_por_pedido=buscar_pagamento_por_pedido)


@admin_bp.route("/pedidos/<int:pedido_id>")
def detalhe_pedido_admin_page(pedido_id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    pedido = ver_detalhe_pedido_admin(pedido_id)

    if not pedido:
        return "Pedido não encontrado"

    return render_template("admin/pedido_detalhe.html", pedido=pedido)


@admin_bp.route("/pedidos/<int:pedido_id>/comprovante")
def comprovante_pedido_admin_page(pedido_id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    pedido = ver_detalhe_pedido_admin(pedido_id)

    if not pedido:
        return "Pedido não encontrado"

    return render_template("admin/pedido_comprovante.html", pedido=pedido)


@admin_bp.route("/pedidos/status/<int:id>/<status>")
def atualizar_status_pedido(id, status):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    status_validos = [
        "AGUARDANDO_PAGAMENTO",
        "PAGO",
        "EM_SEPARACAO",
        "ENVIADO",
        "ENTREGUE",
        "CANCELADO",
        "FALHA_PAGAMENTO",
    ]

    if status not in status_validos:
        return "Status inválido"

    alterar_status(id, status)

    return redirect("/admin/pedidos")


@admin_bp.route("/categorias")
def categorias_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    lista = listar_categorias_admin()

    return render_template("admin/categorias.html", categorias=lista)


@admin_bp.route("/categorias/nova", methods=["GET", "POST"])
def nova_categoria():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        nome = request.form["nome"]
        imagem = request.files.get("imagem")

        imagem_url = None

        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)
            imagem_url = nome_arquivo

        criar_categoria_admin(nome, imagem_url)

        return redirect("/admin/categorias")

    return render_template("admin/nova_categoria.html")


@admin_bp.route("/produtos/<int:id>/estoque", methods=["GET", "POST"])
def estoque_produto(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        tamanho_id = request.form["tamanho"]
        quantidade = request.form["quantidade"]

        estoque(id, tamanho_id, quantidade)

        return redirect("/admin/produtos")

    lista_tamanhos = tamanhos()

    return render_template(
        "admin/estoque_produto.html", tamanhos=lista_tamanhos, produto_id=id
    )


@admin_bp.route("/configuracoes", methods=["GET", "POST"])
def configuracoes_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    config = obter_configuracoes_controller()

    if request.method == "POST":
        nome_loja = request.form["nome_loja"].strip()
        slogan = request.form["slogan"].strip()
        email_contato = request.form["email_contato"].strip()
        whatsapp = request.form["whatsapp"].strip()
        texto_rodape = request.form["texto_rodape"].strip()
        mostrar_credito = True if request.form.get("mostrar_credito") else False
        cor_primaria = request.form["cor_primaria"]
        cor_secundaria = request.form["cor_secundaria"]
        cidade_loja = request.form["cidade_loja"].strip()
        estado_loja = request.form["estado_loja"].strip().upper()

        cor_fundo = request.form["cor_fundo"]
        cor_fundo_secundario = request.form["cor_fundo_secundario"]
        cor_texto = request.form["cor_texto"]
        cor_texto_secundario = request.form["cor_texto_secundario"]

        logo_url = config[14] if config and len(config) > 14 else None

        logo = request.files.get("logo")
        if logo and logo.filename:
            nome_arquivo = secure_filename(logo.filename)
            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
            logo.save(caminho)
            logo_url = nome_arquivo

        salvar_configuracoes_controller(
            nome_loja,
            slogan,
            email_contato,
            whatsapp,
            texto_rodape,
            cor_primaria,
            cor_secundaria,
            cidade_loja,
            estado_loja,
            cor_fundo,
            cor_fundo_secundario,
            cor_texto,
            cor_texto_secundario,
            logo_url,
            mostrar_credito,
        )

        return redirect("/admin/configuracoes")

    return render_template("admin/configuracoes.html", config=config)


@admin_bp.route("/produtos/<int:id>/imagens", methods=["GET", "POST"])
def gerenciar_imagens(id):

    if not admin_logado():
        return redirect("/login")

    if request.method == "POST":

        imagem = request.files["imagem"]

        if imagem:
            nome = secure_filename(imagem.filename)

            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome)

            imagem.save(caminho)

            adicionar_imagem(id, nome)

    imagens = listar_imagens(id)

    return render_template("admin/imagens_produto.html", imagens=imagens, produto_id=id)


@admin_bp.route("/produtos/imagem/excluir/<int:id>/<int:produto_id>")
def excluir_imagem_produto(id, produto_id):

    excluir_imagem(id)

    return redirect(f"/admin/produtos/{produto_id}/imagens")


@admin_bp.route("/produtos/imagem/principal/<int:id>/<int:produto_id>")
def definir_principal_produto(id, produto_id):

    definir_principal(produto_id, id)

    return redirect(f"/admin/produtos/{produto_id}/imagens")


@admin_bp.route("/cupons")
def cupons_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    cupons = listar_cupons_controller()

    return render_template("admin/cupons.html", cupons=cupons)


@admin_bp.route("/cupons/novo", methods=["GET", "POST"])
def novo_cupom_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        codigo = request.form["codigo"]
        tipo = request.form["tipo"]
        valor = request.form["valor"]
        valor_minimo = request.form["valor_minimo"]
        limite_uso = request.form["limite_uso"]
        ativo = request.form["ativo"] == "true"
        data_inicio = request.form["data_inicio"] or None
        data_fim = request.form["data_fim"] or None

        criar_cupom_controller(
            codigo, tipo, valor, valor_minimo, limite_uso, ativo, data_inicio, data_fim
        )

        return redirect("/admin/cupons")

    return render_template("admin/novo_cupom.html")


@admin_bp.route("/cupons/editar/<int:id>", methods=["GET", "POST"])
def editar_cupom_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        codigo = request.form["codigo"]
        tipo = request.form["tipo"]
        valor = request.form["valor"]
        valor_minimo = request.form["valor_minimo"]
        limite_uso = request.form["limite_uso"]
        ativo = request.form["ativo"] == "true"
        data_inicio = request.form["data_inicio"] or None
        data_fim = request.form["data_fim"] or None

        editar_cupom_controller(
            id,
            codigo,
            tipo,
            valor,
            valor_minimo,
            limite_uso,
            ativo,
            data_inicio,
            data_fim,
        )

        return redirect("/admin/cupons")

    cupom = obter_cupom_controller(id)

    return render_template("admin/editar_cupom.html", cupom=cupom)


@admin_bp.route("/cupons/excluir/<int:id>")
def excluir_cupom_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    excluir_cupom_controller(id)

    return redirect("/admin/cupons")


@admin_bp.route("/banners")
def banners_admin_page():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    banners = listar_banners_admin_controller()

    return render_template("admin/banners.html", banners=banners)


@admin_bp.route("/banners/novo", methods=["GET", "POST"])
def novo_banner_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        titulo = request.form["titulo"]
        subtitulo = request.form["subtitulo"]
        link = request.form["link"]
        ativo = request.form["ativo"] == "true"
        ordem = request.form["ordem"]

        imagem = request.files["imagem"]
        imagem_url = None

        if imagem:
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)
            imagem_url = nome_arquivo

        criar_banner_controller(titulo, subtitulo, imagem_url, link, ativo, ordem)

        return redirect("/admin/banners")

    return render_template("admin/novo_banner.html")


@admin_bp.route("/banners/editar/<int:id>", methods=["GET", "POST"])
def editar_banner_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    banner = obter_banner_controller(id)

    if request.method == "POST":

        titulo = request.form["titulo"]
        subtitulo = request.form["subtitulo"]
        link = request.form["link"]
        ativo = request.form["ativo"] == "true"
        ordem = request.form["ordem"]

        imagem = request.files["imagem"]
        imagem_url = banner[3]

        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)
            imagem_url = nome_arquivo

        editar_banner_controller(id, titulo, subtitulo, imagem_url, link, ativo, ordem)

        return redirect("/admin/banners")

    return render_template("admin/editar_banner.html", banner=banner)


@admin_bp.route("/banners/excluir/<int:id>")
def excluir_banner_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    excluir_banner_controller(id)

    return redirect("/admin/banners")


@admin_bp.route("/fretes")
def fretes_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    fretes = listar_fretes_controller()

    return render_template("admin/fretes.html", fretes=fretes)


@admin_bp.route("/fretes/novo", methods=["GET", "POST"])
def novo_frete_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        nome_regiao = request.form["nome_regiao"]
        cep_inicio = request.form["cep_inicio"]
        cep_fim = request.form["cep_fim"]
        valor = request.form["valor"]
        prazo_dias = request.form["prazo_dias"]
        ativo = request.form["ativo"] == "true"

        criar_frete_controller(
            nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo
        )

        return redirect("/admin/fretes")

    return render_template("admin/novo_frete.html")


@admin_bp.route("/fretes/editar/<int:id>", methods=["GET", "POST"])
def editar_frete_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":

        nome_regiao = request.form["nome_regiao"]
        cep_inicio = request.form["cep_inicio"]
        cep_fim = request.form["cep_fim"]
        valor = request.form["valor"]
        prazo_dias = request.form["prazo_dias"]
        ativo = request.form["ativo"] == "true"

        editar_frete_controller(
            id, nome_regiao, cep_inicio, cep_fim, valor, prazo_dias, ativo
        )

        return redirect("/admin/fretes")

    frete = obter_frete_controller(id)

    return render_template("admin/editar_frete.html", frete=frete)


@admin_bp.route("/fretes/excluir/<int:id>")
def excluir_frete_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    excluir_frete_controller(id)

    return redirect("/admin/fretes")


@admin_bp.route("/modalidades-entrega")
def modalidades_entrega_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    modalidades = listar_modalidades_controller()

    return render_template("admin/modalidades_entrega.html", modalidades=modalidades)


@admin_bp.route("/modalidades-entrega/nova", methods=["GET", "POST"])
def nova_modalidade_entrega_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        cidade = request.form["cidade"] or None
        estado = request.form["estado"] or None
        valor = request.form["valor"]
        prazo_horas = request.form["prazo_horas"] or None
        prazo_dias = request.form["prazo_dias"] or None
        ativo = request.form["ativo"] == "true"

        criar_modalidade_controller(
            nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
        )

        return redirect("/admin/modalidades-entrega")

    return render_template("admin/nova_modalidade_entrega.html")


@admin_bp.route("/modalidades-entrega/editar/<int:id>", methods=["GET", "POST"])
def editar_modalidade_entrega_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        cidade = request.form["cidade"] or None
        estado = request.form["estado"] or None
        valor = request.form["valor"]
        prazo_horas = request.form["prazo_horas"] or None
        prazo_dias = request.form["prazo_dias"] or None
        ativo = request.form["ativo"] == "true"

        editar_modalidade_controller(
            id, nome, tipo, cidade, estado, valor, prazo_horas, prazo_dias, ativo
        )

        return redirect("/admin/modalidades-entrega")

    modalidade = obter_modalidade_controller(id)

    return render_template(
        "admin/editar_modalidade_entrega.html", modalidade=modalidade
    )


@admin_bp.route("/modalidades-entrega/excluir/<int:id>")
def excluir_modalidade_entrega_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    excluir_modalidade_controller(id)

    return redirect("/admin/modalidades-entrega")


@admin_bp.route("/home-blocos")
def home_blocos_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    blocos = listar_blocos_home_controller()

    return render_template("admin/home_blocos.html", blocos=blocos)


@admin_bp.route("/home-blocos/novo", methods=["GET", "POST"])
def novo_bloco_home_admin():

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    if request.method == "POST":
        nome = request.form["nome"].strip()
        tipo_bloco = request.form["tipo_bloco"]
        layout = request.form["layout"]
        titulo = request.form["titulo"].strip()
        subtitulo = request.form["subtitulo"].strip()
        descricao = request.form["descricao"].strip()
        texto_botao = request.form["texto_botao"].strip()
        link_botao = request.form["link_botao"].strip()
        texto_botao_secundario = request.form["texto_botao_secundario"].strip()
        link_botao_secundario = request.form["link_botao_secundario"].strip()
        cor_fundo = request.form["cor_fundo"] or None
        cor_texto = request.form["cor_texto"] or None
        alinhamento_texto = request.form["alinhamento_texto"]
        ordem = int(request.form["ordem"])
        ativo = request.form["ativo"] == "true"

        imagem = request.files.get("imagem")
        imagem_url = None

        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)
            imagem_url = nome_arquivo

        criar_bloco_home_controller(
            nome,
            tipo_bloco,
            layout,
            titulo,
            subtitulo,
            descricao,
            imagem_url,
            texto_botao,
            link_botao,
            texto_botao_secundario,
            link_botao_secundario,
            cor_fundo,
            cor_texto,
            alinhamento_texto,
            ordem,
            ativo,
        )

        return redirect("/admin/home-blocos")

    return render_template("admin/novo_home_bloco.html")


@admin_bp.route("/home-blocos/editar/<int:id>", methods=["GET", "POST"])
def editar_bloco_home_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    bloco = obter_bloco_home_controller(id)

    if request.method == "POST":
        nome = request.form["nome"].strip()
        tipo_bloco = request.form["tipo_bloco"]
        layout = request.form["layout"]
        titulo = request.form["titulo"].strip()
        subtitulo = request.form["subtitulo"].strip()
        descricao = request.form["descricao"].strip()
        texto_botao = request.form["texto_botao"].strip()
        link_botao = request.form["link_botao"].strip()
        texto_botao_secundario = request.form["texto_botao_secundario"].strip()
        link_botao_secundario = request.form["link_botao_secundario"].strip()
        cor_fundo = request.form["cor_fundo"] or None
        cor_texto = request.form["cor_texto"] or None
        alinhamento_texto = request.form["alinhamento_texto"]
        ordem = int(request.form["ordem"])
        ativo = request.form["ativo"] == "true"

        imagem_url = bloco[7]

        imagem = request.files.get("imagem")
        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)
            imagem_url = nome_arquivo

        editar_bloco_home_controller(
            id,
            nome,
            tipo_bloco,
            layout,
            titulo,
            subtitulo,
            descricao,
            imagem_url,
            texto_botao,
            link_botao,
            texto_botao_secundario,
            link_botao_secundario,
            cor_fundo,
            cor_texto,
            alinhamento_texto,
            ordem,
            ativo,
        )

        return redirect("/admin/home-blocos")

    return render_template("admin/editar_home_bloco.html", bloco=bloco)


@admin_bp.route("/home-blocos/excluir/<int:id>")
def excluir_bloco_home_admin(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    excluir_bloco_home_controller(id)

    return redirect("/admin/home-blocos")


@admin_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
def editar_categoria_page(id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    categoria = obter_categoria_admin(id)

    if request.method == "POST":
        nome = request.form["nome"]
        imagem = request.files.get("imagem")

        imagem_url = categoria[2]

        if imagem and imagem.filename:
            nome_arquivo = secure_filename(imagem.filename)
            caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], nome_arquivo)
            imagem.save(caminho)
            imagem_url = nome_arquivo

        editar_categoria_admin(id, nome, imagem_url)

        return redirect("/admin/categorias")

    return render_template("admin/editar_categoria.html", categoria=categoria)


@admin_bp.route("/pagamentos/aprovar/<int:pedido_id>")
def aprovar_pagamento(pedido_id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    pagamento = buscar_pagamento_por_pedido(pedido_id)

    if pagamento:
        atualizar_status_pagamento(pagamento["id"], "PAGO")
        atualizar_status_pedido_db(pedido_id, "PAGO")

    return redirect("/admin/pedidos")


@admin_bp.route("/pagamentos/recusar/<int:pedido_id>")
def recusar_pagamento(pedido_id):

    if not usuario_logado():
        return redirect("/login")

    if not admin_logado():
        return redirect("/produtos")

    pagamento = buscar_pagamento_por_pedido(pedido_id)

    if pagamento:
        atualizar_status_pagamento(pagamento["id"], "RECUSADO")
        atualizar_status_pedido_db(pedido_id, "FALHA_PAGAMENTO")

    return redirect("/admin/pedidos")
