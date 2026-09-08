from datetime import datetime, timezone

from app.extensions import db


class MediaPhoto(db.Model):
    __tablename__ = "media_photos"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=True,
    )

    image_path = db.Column(
        db.String(500),
        nullable=True,
    )

    image_url = db.Column(
        db.String(1000),
        nullable=True,
    )

    source_url = db.Column(
        db.String(1000),
        nullable=True,
    )

    photographer = db.Column(
        db.String(200),
        nullable=True,
    )

    event_name = db.Column(
        db.String(200),
        nullable=True,
    )

    event_date = db.Column(
        db.Date,
        nullable=True,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    is_published = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

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
        return f"<MediaPhoto {self.id}: {self.image_path}>"
