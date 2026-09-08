from app.extensions import db


class ReleaseTrack(db.Model):
    __tablename__ = "release_tracks"

    id = db.Column(db.Integer, primary_key=True)

    release_id = db.Column(
        db.Integer,
        db.ForeignKey("releases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    track_number = db.Column(
        db.Integer,
        nullable=False,
    )

    title = db.Column(
        db.String(250),
        nullable=False,
    )

    duration_seconds = db.Column(
        db.Integer,
        nullable=True,
    )

    def __repr__(self):
        return f"<ReleaseTrack {self.release_id}: {self.track_number}. {self.title}>"
