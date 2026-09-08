from datetime import datetime, timezone

from app.extensions import db


class Release(db.Model):
    __tablename__ = "releases"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    release_type = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=True)

    description = db.Column(db.Text, nullable=True)

    cover_image = db.Column(db.String(500), nullable=True)

    bandcamp_url = db.Column(db.String(500), nullable=True)
    spotify_url = db.Column(db.String(500), nullable=True)
    youtube_url = db.Column(db.String(500), nullable=True)
    other_url = db.Column(db.String(500), nullable=True)
    other_url_label = db.Column(db.String(100), nullable=True)

    artwork_credit = db.Column(db.String(250), nullable=True)

    label = db.Column(db.String(250), nullable=True)
    catalog_number = db.Column(db.String(100), nullable=True)
    format = db.Column(db.String(100), nullable=True)
    release_date = db.Column(db.Date, nullable=True)

    lineup = db.Column(db.Text, nullable=True)
    recording_info = db.Column(db.Text, nullable=True)

    engineering_credit = db.Column(db.String(250), nullable=True)
    mixing_mastering_credit = db.Column(db.String(250), nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

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

    tracks = db.relationship(
        "ReleaseTrack",
        backref="release",
        cascade="all, delete-orphan",
        order_by="ReleaseTrack.track_number",
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
        return f"<Release {self.id}: {self.title}>"
