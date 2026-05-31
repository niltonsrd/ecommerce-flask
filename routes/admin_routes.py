"""
Compatibilidade com imports legados.

As rotas admin foram divididas em blueprints especializados em routes/admin/.
Novos registros devem importar esses blueprints diretamente em app.py.
"""

from routes.admin.admin_dashboard_routes import admin_dashboard_bp as admin_bp

__all__ = ["admin_bp"]
