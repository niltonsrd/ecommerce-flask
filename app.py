import os
from flask import Flask, session, render_template
from routes.auth_routes import auth_bp
from routes.produto_routes import produto_bp
from routes.carrinho_routes import carrinho_bp
from routes.pedido_routes import pedido_bp
from routes.admin_routes import admin_bp
from routes.favorito_routes import favorito_bp
from routes.checkout_routes import checkout_bp
from routes.endereco_routes import endereco_bp

from controllers.configuracao_controller import obter_configuracoes_controller
from controllers.carrinho_controller import total_itens_carrinho, obter_mini_carrinho
from controllers.banner_controller import listar_banners_site_controller
from controllers.produto_controller import listar
from controllers.home_bloco_controller import listar_blocos_home_ativos_controller
from services.categoria_service import categorias
from utils.theme_utils import hex_to_rgb_string


app = Flask(__name__)

app.secret_key = "segredo_super_secreto"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.register_blueprint(auth_bp)
app.register_blueprint(produto_bp)
app.register_blueprint(carrinho_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(favorito_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(endereco_bp)


@app.context_processor
def inject_configuracoes():
    config = obter_configuracoes_controller()

    total_carrinho = 0
    mini_carrinho_itens = []
    mini_carrinho_total = 0

    usuario_id = session.get("usuario_id")

    if usuario_id:
        total_carrinho = total_itens_carrinho(usuario_id)

        mini_carrinho = obter_mini_carrinho(usuario_id)
        mini_carrinho_itens = mini_carrinho["itens"]
        mini_carrinho_total = mini_carrinho["total"]

    menu_categorias = categorias()

    cor_primaria = "#6366f1"
    cor_secundaria = "#a855f7"
    cor_fundo = "#06080f"
    cor_fundo_secundario = "#090d16"
    cor_texto = "#f8fafc"
    cor_texto_secundario = "#94a3b8"
    logo_url = None

    if config:
        if config[6]:
            cor_primaria = config[6]
        if config[7]:
            cor_secundaria = config[7]
        if config[10]:
            cor_fundo = config[10]
        if config[11]:
            cor_fundo_secundario = config[11]
        if config[12]:
            cor_texto = config[12]
        if config[13]:
            cor_texto_secundario = config[13]
        if config[14]:
            logo_url = config[14]

    return {
        "config_loja": config,
        "total_carrinho": total_carrinho,
        "mini_carrinho_itens": mini_carrinho_itens,
        "mini_carrinho_total": mini_carrinho_total,
        "menu_categorias": menu_categorias,
        "cor_primaria": cor_primaria,
        "cor_secundaria": cor_secundaria,
        "cor_primaria_rgb": hex_to_rgb_string(cor_primaria),
        "cor_secundaria_rgb": hex_to_rgb_string(cor_secundaria),
        "cor_fundo": cor_fundo,
        "cor_fundo_secundario": cor_fundo_secundario,
        "cor_texto": cor_texto,
        "cor_texto_secundario": cor_texto_secundario,
        "logo_url": logo_url,
    }


@app.route("/")
def home():
    blocos_home = listar_blocos_home_ativos_controller()
    produtos = listar()
    
    print("PRODUTOS HOME:", produtos[:3])  # Debug: Verificar os produtos retornados    

    return render_template(
        "loja/home.html", blocos_home=blocos_home, produtos=produtos[:8]
    )


if __name__ == "__main__":
    app.run(debug=True)
