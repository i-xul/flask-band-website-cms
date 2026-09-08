import os
from datetime import datetime, timezone

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from app.admin import admin_bp
from app.auth import auth_bp
from app.extensions import csrf, db, limiter, login_manager, migrate
from app.public import public_bp
from config import DevelopmentConfig, ProductionConfig


def create_app(config_class=None):
    if config_class is None:
        environment = os.environ.get(
            "APP_ENV",
            "development",
        ).lower()

        if environment == "production":
            config_class = ProductionConfig
        else:
            config_class = DevelopmentConfig

    app = Flask(__name__)

    app.config.from_object(config_class)

    if app.config["ENVIRONMENT"] == "production":
        if not app.config.get("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY must be set in the production environment.")

        ratelimit_storage_uri = app.config.get("RATELIMIT_STORAGE_URI")

        if not ratelimit_storage_uri:
            raise RuntimeError(
                "RATELIMIT_STORAGE_URI must be set in the production environment."
            )

        if ratelimit_storage_uri == "memory://":
            raise RuntimeError(
                "RATELIMIT_STORAGE_URI cannot use memory:// in production."
            )

        if not app.config.get("TRUSTED_HOSTS"):
            raise RuntimeError(
                "TRUSTED_HOSTS must be set in the production environment."
            )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access the administration area."

    from app import models  # noqa: F401
    from app.commands import create_admin, seed_demo

    app.cli.add_command(seed_demo)
    app.cli.add_command(create_admin)

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    @app.after_request
    def add_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "font-src 'self'; "
            "img-src 'self' https: data:; "
            "frame-src https://www.youtube-nocookie.com; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'"
        )

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response

    @app.context_processor
    def inject_footer_data():
        from app.models import ContactInfo

        footer_contact_info = ContactInfo.query.first()
        current_year = datetime.now(timezone.utc).year

        return {
            "footer_contact_info": footer_contact_info,
            "current_year": current_year,
        }

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500

    if app.config.get("USE_PROXY_FIX"):
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=1,
            x_proto=1,
            x_host=1,
        )

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    return db.session.get(User, int(user_id))
