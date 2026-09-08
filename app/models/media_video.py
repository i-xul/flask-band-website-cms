from datetime import datetime, timezone

from app.extensions import db


class MediaVideo(db.Model):
    __tablename__ = "media_videos"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False,
    )

    youtube_url = db.Column(
        db.String(500),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    year = db.Column(
        db.Integer,
        nullable=True,
    )

    is_published = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=0,
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
        return f"<MediaVideo {self.id}: {self.title}>"
