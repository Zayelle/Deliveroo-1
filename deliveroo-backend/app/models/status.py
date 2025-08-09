from app.extensions import db

from datetime import datetime

class Status(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    parcels = db.relationship('Parcel', back_populates='status', lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    def __repr__(self):
        return f"<Status {self.name}>"
