from flask import Blueprint, render_template, session, redirect
from middlewares.auth import admin_required
from controllers.admin_dashboard_controller import dashboard_admin

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, url_prefix="/admin")


@admin_dashboard_bp.route("/")
@admin_required
def dashboard():
    dados_dashboard = dashboard_admin()
    return render_template("admin/dashboard.html", dashboard=dados_dashboard)
