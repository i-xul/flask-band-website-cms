from datetime import date, datetime, timezone

import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models import News, Show, User


@click.command("seed-demo")
@with_appcontext
def seed_demo():
    """Add temporary development-only content to the database."""

    existing_news = News.query.filter_by(
        title="Demo band website launched"
    ).first()

    if existing_news is None:
        news = News(
            title="Demo band website launched",
            short_text="The demo band's new website is now online.",
            body=(
                "This is temporary development content used to test "
                "the website content pipeline."
            ),
            is_published=True,
            is_featured=True,
            published_at=datetime.now(timezone.utc),
        )
        db.session.add(news)

    existing_show = Show.query.filter_by(
        venue="Development Test Venue",
        city="Helsinki",
    ).first()

    if existing_show is None:
        show = Show(
            show_date=date(2027, 9, 12),
            venue="Development Test Venue",
            city="Helsinki",
            country="Finland",
            other_bands="Test Support Band",
            notes="Temporary development show.",
            is_published=True,
        )
        db.session.add(show)

    db.session.commit()

    click.echo("Development-only demo content added.")


@click.command("create-admin")
@click.argument("username")
@with_appcontext
def create_admin(username):
    """Create an administrator account."""

    username = username.strip()

    existing_user = User.query.filter_by(username=username).first()

    if existing_user is not None:
        raise click.ClickException(f"User '{username}' already exists.")

    password = click.prompt(
        "Password",
        hide_input=True,
        confirmation_prompt=True,
    )

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    click.echo(f"Admin user '{username}' created.")
