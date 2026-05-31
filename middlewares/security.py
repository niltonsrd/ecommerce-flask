import os
import secrets
import time
from collections import defaultdict
from functools import wraps
from hmac import compare_digest
from pathlib import Path

from flask import current_app, jsonify, render_template, request, session
from PIL import Image, UnidentifiedImageError


_rate_limit_store = defaultdict(list)

IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
DOCUMENT_EXTENSIONS = {"pdf"}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | DOCUMENT_EXTENSIONS
ALLOWED_MIMETYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
    "gif": "image/gif",
    "pdf": "application/pdf",
}
MAX_FILE_SIZE = 5 * 1024 * 1024


def _is_ajax_request():
    return request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _client_ip():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _rate_key(namespace, identifier=None):
    return f"{namespace}:{identifier or _client_ip()}"


def _prune_rate_key(key, window_seconds):
    now = time.time()
    _rate_limit_store[key] = [
        timestamp for timestamp in _rate_limit_store[key]
        if now - timestamp < window_seconds
    ]
    return now


def rate_limit(max_requests=60, window_seconds=60, namespace=None, methods=None):
    allowed_methods = {method.upper() for method in methods} if methods else None

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if allowed_methods and request.method.upper() not in allowed_methods:
                return f(*args, **kwargs)

            key = _rate_key(namespace or f.__name__)
            now = _prune_rate_key(key, window_seconds)

            if len(_rate_limit_store[key]) >= max_requests:
                if _is_ajax_request():
                    return jsonify({
                        "ok": False,
                        "message": "Muitas requisições. Tente novamente mais tarde.",
                    }), 429
                return render_template("errors/429.html"), 429

            _rate_limit_store[key].append(now)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def login_rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method.upper() != "POST":
            return f(*args, **kwargs)

        key = _rate_key("login")
        now = _prune_rate_key(key, 300)

        if len(_rate_limit_store[key]) >= 5:
            if _is_ajax_request():
                return jsonify({
                    "ok": False,
                    "message": "Muitas tentativas de login. Aguarde 5 minutos.",
                }), 429
            return render_template(
                "auth/login.html",
                erro="Muitas tentativas de login. Aguarde 5 minutos.",
            ), 429

        _rate_limit_store[key].append(now)
        return f(*args, **kwargs)

    return decorated_function


def reset_login_rate_limit():
    _rate_limit_store.pop(_rate_key("login"), None)


def csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def csrf_protect():
    if request.method.upper() not in {"POST", "PUT", "PATCH", "DELETE"}:
        return None

    sent_token = (
        request.form.get("csrf_token")
        or request.headers.get("X-CSRFToken")
        or request.headers.get("X-CSRF-Token")
    )
    expected_token = session.get("_csrf_token")

    if not sent_token or not expected_token or not compare_digest(sent_token, expected_token):
        if _is_ajax_request():
            return jsonify({"ok": False, "message": "Token CSRF inválido."}), 400
        return render_template("errors/400.html", mensagem="Token CSRF inválido."), 400

    return None


def apply_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-XSS-Protection", "1; mode=block")
    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=(), payment=()",
    )
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' https://viacep.com.br; "
        "frame-ancestors 'self'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )
    return response


def arquivo_permitido(filename, allowed_extensions=None):
    allowed = allowed_extensions or ALLOWED_EXTENSIONS
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed


def _file_size(file_storage):
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    return size


def _validar_assinatura(file_storage, extensao):
    head = file_storage.stream.read(8192)
    file_storage.stream.seek(0)

    if extensao == "pdf":
        return head.startswith(b"%PDF")

    try:
        with Image.open(file_storage.stream) as image:
            image.verify()
            formato = (image.format or "").lower()
    except (UnidentifiedImageError, OSError):
        file_storage.stream.seek(0)
        return False
    finally:
        file_storage.stream.seek(0)

    formatos_validos = {
        "jpg": {"jpeg"},
        "jpeg": {"jpeg"},
        "png": {"png"},
        "webp": {"webp"},
        "gif": {"gif"},
    }
    return formato in formatos_validos.get(extensao, set())


def validar_arquivo(file_storage, allowed_extensions=None, max_size=None):
    allowed = allowed_extensions or ALLOWED_EXTENSIONS
    max_bytes = max_size or MAX_FILE_SIZE

    if not file_storage or not file_storage.filename:
        return False, "Nenhum arquivo enviado."

    if not arquivo_permitido(file_storage.filename, allowed):
        return False, "Formato de arquivo não permitido."

    extensao = file_storage.filename.rsplit(".", 1)[1].lower()
    tamanho = _file_size(file_storage)

    if tamanho > max_bytes:
        return False, f"Arquivo muito grande. Máximo permitido: {max_bytes // (1024 * 1024)}MB."

    mimetype_esperado = ALLOWED_MIMETYPES.get(extensao)
    mimetype_enviado = (file_storage.mimetype or "").lower()
    if mimetype_enviado and mimetype_esperado and mimetype_enviado != mimetype_esperado:
        if not (
            extensao in {"jpg", "jpeg"}
            and mimetype_enviado in {"image/pjpeg", "image/jpeg", "image/jpg"}
        ):
            return False, "Tipo MIME incompatível com a extensão enviada."

    if not _validar_assinatura(file_storage, extensao):
        return False, "Conteúdo do arquivo não corresponde ao formato informado."

    return True, None


def gerar_nome_seguro(prefixo, extensao):
    safe_prefix = "".join(ch for ch in prefixo.lower() if ch.isalnum() or ch in {"-", "_"})
    safe_prefix = safe_prefix.strip("_-") or "arquivo"
    return f"{safe_prefix}_{secrets.token_hex(16)}.{extensao.lower().lstrip('.')}"


def salvar_upload(file_storage, prefixo, subdiretorio="", allowed_extensions=None, max_size=None):
    valido, erro = validar_arquivo(
        file_storage,
        allowed_extensions=allowed_extensions,
        max_size=max_size,
    )
    if not valido:
        raise ValueError(erro)

    extensao = file_storage.filename.rsplit(".", 1)[1].lower()
    nome_arquivo = gerar_nome_seguro(prefixo, extensao)

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    if not upload_folder.is_absolute():
        upload_folder = Path(current_app.root_path) / upload_folder

    destino_dir = (upload_folder / subdiretorio).resolve()
    upload_root = upload_folder.resolve()
    if upload_root not in destino_dir.parents and destino_dir != upload_root:
        raise ValueError("Diretório de upload inválido.")

    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / nome_arquivo
    file_storage.save(destino)

    if subdiretorio:
        return f"{subdiretorio.strip('/').strip(os.sep)}/{nome_arquivo}".replace("\\", "/")
    return nome_arquivo
