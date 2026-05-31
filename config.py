import os

from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", os.getenv("FLASK_ENV", "development")).lower()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "ecommerce")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DATABASE_URL = os.getenv("DATABASE_URL")

_SECRET_KEY = os.getenv("SECRET_KEY")
if not _SECRET_KEY:
    if APP_ENV == "production":
        raise RuntimeError("SECRET_KEY deve ser configurada em produção.")
    _SECRET_KEY = os.urandom(64).hex()

SECRET_KEY = _SECRET_KEY
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploads")
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
SESSION_COOKIE_SECURE = os.getenv(
    "SESSION_COOKIE_SECURE", "True" if APP_ENV == "production" else "False"
).lower() in ("true", "1", "yes")
PERMANENT_SESSION_LIFETIME = int(os.getenv("SESSION_LIFETIME", 86400))

DB_POOL_MIN = int(os.getenv("DB_POOL_MIN", 2))
DB_POOL_MAX = int(os.getenv("DB_POOL_MAX", 10))

RATE_LIMIT_DEFAULT = int(os.getenv("RATE_LIMIT_DEFAULT", 240))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))
RUN_MIGRATIONS_ON_START = os.getenv("RUN_MIGRATIONS_ON_START", "False").lower() in (
    "true",
    "1",
    "yes",
)
