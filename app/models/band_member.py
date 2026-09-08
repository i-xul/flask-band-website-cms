from datetime import datetime, timezone

from app.extensions import db


class BandMember(db.Model):
    __tablename__ = "band_members"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    slug = db.Column(
        db.String(200),
        nullable=True,
        unique=True,
        index=True,
    )

    role = db.Column(db.String(200), nullable=False)

    image = db.Column(db.String(500), nullable=True)

    bio = db.Column(db.Text, nullable=True)

    other_projects = db.Column(db.Text, nullable=True)

    stage_setup = db.Column(db.Text, nullable=True)

    studio_setup = db.Column(db.Text, nullable=True)

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    activities = db.relationship(
        "BandMemberActivity",
        backref="band_member",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="BandMemberActivity.sort_order, BandMemberActivity.start_year",
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
        return f"<BandMember {self.id}: {self.name}>"
