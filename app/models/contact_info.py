from datetime import datetime, timezone

from app.extensions import db


class ContactInfo(db.Model):
    __tablename__ = "contact_info"

    id = db.Column(db.Integer, primary_key=True)

    intro = db.Column(
        db.Text,
        nullable=True,
    )

    general_email = db.Column(
        db.String(250),
        nullable=True,
    )

    booking_email = db.Column(
        db.String(250),
        nullable=True,
    )

    press_email = db.Column(
        db.String(250),
        nullable=True,
    )

    facebook_url = db.Column(
        db.String(500),
        nullable=True,
    )

    instagram_url = db.Column(
        db.String(500),
        nullable=True,
    )

    youtube_url = db.Column(
        db.String(500),
        nullable=True,
    )

    bandcamp_url = db.Column(
        db.String(500),
        nullable=True,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<ContactInfo {self.id}>"
