from app.extensions import db
from datetime import datetime

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

     # Parcels sent *from* this location
    parcels = db.relationship('Parcel', foreign_keys='Parcel.origin_id', back_populates='origin', lazy=True)

    # Parcels being delivered *to* this location
    destination_parcels = db.relationship('Parcel', foreign_keys='Parcel.destination_id', back_populates='destination', lazy=True)

    # Parcels currently *present* at this location
    present_parcels = db.relationship('Parcel', foreign_keys='Parcel.present_location_id', back_populates='present_location', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

