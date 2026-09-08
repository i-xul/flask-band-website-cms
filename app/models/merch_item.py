from datetime import datetime, timezone

from app.extensions import db


class MerchItem(db.Model):
    __tablename__ = "merch_items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(200),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    price_cents = db.Column(
        db.Integer,
        nullable=True,
    )

    image_path = db.Column(
        db.String(500),
        nullable=True,
    )

    external_url = db.Column(
        db.String(1000),
        nullable=True,
    )

    availability = db.Column(
        db.String(100),
        nullable=True,
    )

    stock_quantity = db.Column(
        db.Integer,
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
        return f"<MerchItem {self.id}: {self.name}>"
