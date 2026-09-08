from datetime import datetime, timezone

from app.extensions import db


class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)

    show_date = db.Column(db.Date, nullable=False)
    show_time = db.Column(db.Time, nullable=True)

    venue = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(150), nullable=False)

    other_bands = db.Column(db.Text, nullable=True)

    event_url = db.Column(db.String(500), nullable=True)
    ticket_url = db.Column(db.String(500), nullable=True)

    notes = db.Column(db.Text, nullable=True)
    poster_image = db.Column(db.String(500), nullable=True)

    is_published = db.Column(db.Boolean, nullable=False, default=False)
    is_cancelled = db.Column(db.Boolean, nullable=False, default=False)

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
        return f"<Show {self.id}: {self.show_date} {self.city}, {self.country}>"
