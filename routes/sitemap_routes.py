from flask import Blueprint, Response, request
from database.db import get_connection

sitemap_bp = Blueprint("sitemap", __name__)


@sitemap_bp.route("/sitemap.xml")
def sitemap():
    base_url = request.host_url.rstrip("/")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    pages = [
        {"loc": "/", "priority": "1.0"},
        {"loc": "/produtos", "priority": "0.9"},
        {"loc": "/cadastro", "priority": "0.5"},
        {"loc": "/login", "priority": "0.5"},
    ]

    for page in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{base_url}{page['loc']}</loc>")
        lines.append(f"    <priority>{page['priority']}</priority>")
        lines.append("  </url>")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, atualizado_em FROM produtos WHERE ativo = TRUE")
    for row in cursor.fetchall():
        lines.append("  <url>")
        lines.append(f"    <loc>{base_url}/produto/{row[0]}</loc>")
        lines.append("    <priority>0.8</priority>")
        if row[2]:
            lines.append(f"    <lastmod>{row[2].strftime('%Y-%m-%d')}</lastmod>")
        lines.append("  </url>")
    cursor.close()
    conn.close()

    lines.append("</urlset>")
    return Response("\n".join(lines), mimetype="application/xml")


@sitemap_bp.route("/robots.txt")
def robots():
    base_url = request.host_url.rstrip("/")
    content = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /login
Disallow: /cadastro
Disallow: /carrinho
Disallow: /checkout*
Disallow: /meus-pedidos
Disallow: /minha-conta
Disallow: /configuracoes-conta
Disallow: /enderecos
Disallow: /favoritos

Sitemap: {base_url}/sitemap.xml
"""
    return Response(content, mimetype="text/plain")
