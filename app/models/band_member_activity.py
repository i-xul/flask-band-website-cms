"""
Author: H A (i-xul)
Repository: https://github.com/i-xul/flask-band-website-cms
File: app/models/band_member_activity.py
Created: 2026-08-25
Version: 1.0.0

Purpose:
    Store structured role-specific activity periods for band members.

Overview:
    Each record represents one role held by one band member during one
    continuous activity period. A NULL end year represents an activity
    period that is still ongoing.

    Multiple records may exist for the same member and role, allowing
    separate activity periods such as 2013-2015 and 2029-present.
"""

from app.extensions import db

# ---------------------------------------------------------------------------
# Band member activity model
# ---------------------------------------------------------------------------


class BandMemberActivity(db.Model):
    """Represent one role-specific activity period for a band member."""

    __tablename__ = "band_member_activities"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    band_member_id = db.Column(
        db.Integer,
        db.ForeignKey("band_members.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role = db.Column(
        db.String(200),
        nullable=False,
    )

    start_year = db.Column(
        db.Integer,
        nullable=False,
    )

    end_year = db.Column(
        db.Integer,
        nullable=True,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    def __repr__(self):
        return (
            f"<BandMemberActivity {self.id}: "
            f"member={self.band_member_id}, role={self.role}>"
        )
