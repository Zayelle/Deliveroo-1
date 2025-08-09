from app.extensions import db

from datetime import datetime

class Parcel(db.Model):
    __tablename__ = 'parcels'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    present_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    
    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    origin = db.relationship('Location', foreign_keys=[origin_id], back_populates='parcels')
    destination = db.relationship('Location', foreign_keys=[destination_id], back_populates='destination_parcels')
    present_location = db.relationship('Location', foreign_keys=[present_location_id], back_populates='parcels')
    status = db.relationship('Status', back_populates='parcels')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "origin": self.origin.city if self.origin else None,
            "destination": self.destination.city if self.destination else None,
            "present_location": self.present_location.city if self.present_location else None,
            "status": self.status.name if self.status else None,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

