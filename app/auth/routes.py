from urllib.parse import urljoin, urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.auth import auth_bp
from app.auth.forms import LoginForm
from app.extensions import limiter
from app.models import User


def is_safe_redirect_target(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))

    return (
        redirect_url.scheme in {"http", "https"}
        and host_url.netloc == redirect_url.netloc
    )


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next_url = request.args.get("next")

            if next_url and is_safe_redirect_target(next_url):
                return redirect(next_url)

            return redirect(url_for("admin.dashboard"))

        flash("Invalid username or password.", "error")

    return render_template(
        "auth/login.html",
        form=form,
    )


@auth_bp.post("/logout")
def logout():
    logout_user()

    return redirect(url_for("auth.login"))
