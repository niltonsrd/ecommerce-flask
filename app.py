import os
from flask import Flask, session, render_template

from config import (
    SECRET_KEY,
    DEBUG,
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH,
    SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE,
    SESSION_COOKIE_SECURE,
    PERMANENT_SESSION_LIFETIME,
    RUN_MIGRATIONS_ON_START,
)
from database.connection import init_pool, close_pool
from database.migrations import aplicar_migrations
from middlewares.security import apply_security_headers, csrf_protect, csrf_token

from routes.auth_routes import auth_bp
from routes.produto_routes import produto_bp
from routes.carrinho_routes import carrinho_bp
from routes.pedido_routes import pedido_bp
from routes.favorito_routes import favorito_bp
from routes.checkout_routes import checkout_bp
from routes.endereco_routes import endereco_bp
from routes.sitemap_routes import sitemap_bp
from routes.admin.admin_products_routes import admin_products_bp
from routes.admin.admin_orders_routes import admin_orders_bp
from routes.admin.admin_categories_routes import admin_categories_bp
from routes.admin.admin_coupons_routes import admin_coupons_bp
from routes.admin.admin_delivery_routes import admin_delivery_bp
from routes.admin.admin_home_routes import admin_home_bp
from routes.admin.admin_settings_routes import admin_settings_bp
from routes.admin.admin_dashboard_routes import admin_dashboard_bp
from routes.admin.admin_customers_routes import admin_customers_bp

from controllers.configuracao_controller import obter_configuracoes_controller
from controllers.carrinho_controller import (
    obter_mini_carrinho,
    obter_mini_carrinho_anonimo,
    total_itens_carrinho,
    total_itens_carrinho_anonimo,
)
from controllers.produto_controller import listar
from controllers.home_bloco_controller import listar_blocos_home_ativos_controller
from services.carrinho_service import SESSION_CART_KEY
from services.categoria_service import categorias
from utils.theme_utils import hex_to_rgb_string


def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["SESSION_COOKIE_HTTPONLY"] = SESSION_COOKIE_HTTPONLY
    app.config["SESSION_COOKIE_SAMESITE"] = SESSION_COOKIE_SAMESITE
    app.config["SESSION_COOKIE_SECURE"] = SESSION_COOKIE_SECURE
    app.config["PERMANENT_SESSION_LIFETIME"] = PERMANENT_SESSION_LIFETIME

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    if RUN_MIGRATIONS_ON_START:
        aplicar_migrations()

    @app.before_request
    def before_request():
        session.permanent = True
        return csrf_protect()

    @app.after_request
    def after_request(response):
        return apply_security_headers(response)

    register_blueprints(app)
    register_context_processors(app)
    register_error_handlers(app)
    register_routes(app)

    return app


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(carrinho_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(favorito_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(endereco_bp)
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(admin_products_bp)
    app.register_blueprint(admin_orders_bp)
    app.register_blueprint(admin_categories_bp)
    app.register_blueprint(admin_coupons_bp)
    app.register_blueprint(admin_delivery_bp)
    app.register_blueprint(admin_home_bp)
    app.register_blueprint(admin_settings_bp)
    app.register_blueprint(admin_customers_bp)
    app.register_blueprint(sitemap_bp)


def register_context_processors(app):
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
        else:
            carrinho_anonimo = session.get(SESSION_CART_KEY, {})
            total_carrinho = total_itens_carrinho_anonimo(carrinho_anonimo)
            mini_carrinho = obter_mini_carrinho_anonimo(carrinho_anonimo)
            mini_carrinho_itens = mini_carrinho["itens"]
            mini_carrinho_total = mini_carrinho["total"]

        menu_categorias = categorias()

        defaults = {
            "cor_primaria": "#6366f1",
            "cor_secundaria": "#a855f7",
            "cor_fundo": "#06080f",
            "cor_fundo_secundario": "#090d16",
            "cor_texto": "#f8fafc",
            "cor_texto_secundario": "#94a3b8",
            "logo_url": None,
            "background_url": None,
        }

        if config:
            campos = {
                "cor_primaria": 6, "cor_secundaria": 7,
                "cor_fundo": 10, "cor_fundo_secundario": 11,
                "cor_texto": 12, "cor_texto_secundario": 13, "logo_url": 14,
                "background_url": 16,
            }
            for nome, idx in campos.items():
                if idx < len(config) and config[idx]:
                    defaults[nome] = config[idx]

        return {
            "config_loja": config,
            "total_carrinho": total_carrinho,
            "mini_carrinho_itens": mini_carrinho_itens,
            "mini_carrinho_total": mini_carrinho_total,
            "menu_categorias": menu_categorias,
            "cor_primaria": defaults["cor_primaria"],
            "cor_secundaria": defaults["cor_secundaria"],
            "cor_primaria_rgb": hex_to_rgb_string(defaults["cor_primaria"]),
            "cor_secundaria_rgb": hex_to_rgb_string(defaults["cor_secundaria"]),
            "cor_fundo": defaults["cor_fundo"],
            "cor_fundo_secundario": defaults["cor_fundo_secundario"],
            "cor_texto": defaults["cor_texto"],
            "cor_texto_secundario": defaults["cor_texto_secundario"],
            "logo_url": defaults["logo_url"],
            "background_url": defaults["background_url"],
            "csrf_token": csrf_token,
        }


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    @app.errorhandler(429)
    def too_many_requests(e):
        return render_template("errors/429.html"), 429


def register_routes(app):
    @app.route("/")
    def home():
        blocos_home = listar_blocos_home_ativos_controller()
        produtos = listar()
        return render_template(
            "loja/home.html", blocos_home=blocos_home, produtos=produtos[:8]
        )


app = create_app()

if __name__ == "__main__":
    init_pool()
    try:
        app.run(debug=DEBUG, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    finally:
        close_pool()
