"""
Production settings for ERP Terrenos.
"""
import dj_database_url

from .base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="").split(",")  # noqa: F405

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=""),  # noqa: F405
        conn_max_age=600,
    )
}

CORS_ALLOWED_ORIGINS = config(  # noqa: F405
    "CORS_ALLOWED_ORIGINS",
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)  # noqa: F405
