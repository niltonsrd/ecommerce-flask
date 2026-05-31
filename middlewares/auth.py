import functools

from flask import session, redirect, request, jsonify


def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("usuario_id"):
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"ok": False, "redirect": "/login", "message": "Faça login para continuar."}), 401
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("usuario_id"):
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"ok": False, "redirect": "/login", "message": "Faça login para continuar."}), 401
            return redirect("/login")
        if session.get("usuario_tipo") != "admin":
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"ok": False, "message": "Acesso restrito a administradores."}), 403
            return redirect("/produtos")
        return f(*args, **kwargs)
    return decorated_function


def guest_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usuario_id"):
            if session.get("usuario_tipo") == "admin":
                return redirect("/admin")
            return redirect("/produtos")
        return f(*args, **kwargs)
    return decorated_function
