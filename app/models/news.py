from datetime import datetime, timezone

from app.extensions import db


class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    short_text = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=True)

    link_url = db.Column(db.String(500), nullable=True)

    is_published = db.Column(db.Boolean, nullable=False, default=False)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)

    published_at = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<News {self.id}: {self.title}>"
