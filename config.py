import os


def get_trusted_hosts():
    value = os.environ.get("TRUSTED_HOSTS")

    if not value:
        return None

    return [host.strip() for host in value.split(",") if host.strip()]


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///band_website.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_PROXY_FIX = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    IMAGE_UPLOAD_MAX_WIDTH = 2400
    IMAGE_UPLOAD_MAX_HEIGHT = 2400
    IMAGE_UPLOAD_WEBP_QUALITY = 85

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    RATELIMIT_STORAGE_URI = os.environ.get(
        "RATELIMIT_STORAGE_URI",
        "memory://",
    )


class DevelopmentConfig(Config):
    ENVIRONMENT = "development"
    DEBUG = True

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-me",
    )


class ProductionConfig(Config):
    ENVIRONMENT = "production"
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get("SECRET_KEY")
    TRUSTED_HOSTS = get_trusted_hosts()
    USE_PROXY_FIX = True

    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = "https"
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI")
