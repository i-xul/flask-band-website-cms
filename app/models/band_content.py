from datetime import datetime, timezone

from app.extensions import db


class BandContent(db.Model):
    __tablename__ = "band_content"

    id = db.Column(db.Integer, primary_key=True)

    intro = db.Column(db.Text, nullable=True)
    history = db.Column(db.Text, nullable=True)

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<BandContent {self.id}>"
