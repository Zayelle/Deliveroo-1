from flask import jsonify
from app.models.parcel import Parcel
from app.models.user import User
from app.extensions import db

from marshmallow import Schema, fields, ValidationError
from datetime import datetime

# ----------------- Schemas ----------------- #

class ParcelCreateSchema(Schema):
    pickup_location = fields.Str(required=True)
    destination = fields.Str(required=True)
    weight = fields.Float(required=True)

class ParcelUpdateDestinationSchema(Schema):
    destination = fields.Str(required=True)

class ParcelStatusUpdateSchema(Schema):
    status = fields.Str(required=True)

class ParcelLocationUpdateSchema(Schema):
    current_location = fields.Str(required=True)

create_schema = ParcelCreateSchema()
destination_schema = ParcelUpdateDestinationSchema()
status_schema = ParcelStatusUpdateSchema()
location_schema = ParcelLocationUpdateSchema()

# ----------------- User Actions ----------------- #

def create_parcel(user_id, data):
    try:
        validated = create_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    parcel = Parcel(
        user_id=user_id,
        pickup_location=validated['pickup_location'],
        destination=validated['destination'],
        weight=validated['weight'],
        status="Pending",
        current_location=validated['pickup_location'],
        created_at=datetime.utcnow()
    )

    db.session.add(parcel)
    db.session.commit()

    return jsonify({"message": "Parcel created successfully", "parcel_id": parcel.id}), 201

def get_all_user_parcels(user_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    paginated = Parcel.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    return jsonify({
        "parcels": [p.to_dict() for p in paginated.items],
        "total": paginated.total,
        "pages": paginated.pages,
        "page": page
    }), 200


def get_parcel_by_id(user_id, parcel_id):
    parcel = Parcel.query.get(parcel_id)
    if not parcel or parcel.user_id != user_id:
        return jsonify({"error": "Parcel not found"}), 404
    return jsonify(parcel.to_dict()), 200

def update_parcel_destination(user_id, parcel_id, data):
    try:
        validated = destination_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    parcel = Parcel.query.get(parcel_id)
    if not parcel or parcel.user_id != user_id:
        return jsonify({"error": "Parcel not found"}), 404

    if parcel.status.lower() == "delivered":
        return jsonify({"error": "Cannot change destination of delivered parcel"}), 403

    parcel.destination = validated["destination"]
    db.session.commit()
    return jsonify({"message": "Destination updated"}), 200

def cancel_parcel(user_id, parcel_id):
    parcel = Parcel.query.get(parcel_id)
    if not parcel or parcel.user_id != user_id:
        return jsonify({"error": "Parcel not found"}), 404

    if parcel.status.lower() == "delivered":
        return jsonify({"error": "Cannot cancel a delivered parcel"}), 403

    parcel.status = "Cancelled"
    db.session.commit()
    return jsonify({"message": "Parcel cancelled successfully"}), 200

def delete_parcel(user_id, parcel_id):
    parcel = Parcel.query.get(parcel_id)
    if not parcel or parcel.user_id != user_id:
        return jsonify({"error": "Parcel not found"}), 404

    db.session.delete(parcel)
    db.session.commit()
    return jsonify({"message": "Parcel deleted"}), 200

# ----------------- Admin Actions ----------------- #

def admin_update_status(parcel_id, data):
    try:
        validated = status_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    parcel = Parcel.query.get(parcel_id)
    if not parcel:
        return jsonify({"error": "Parcel not found"}), 404

    parcel.status = validated["status"]
    db.session.commit()
    return jsonify({"message": "Status updated"}), 200

def admin_update_location(parcel_id, data):
    try:
        validated = location_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    parcel = Parcel.query.get(parcel_id)
    if not parcel:
        return jsonify({"error": "Parcel not found"}), 404

    parcel.current_location = validated["current_location"]
    db.session.commit()
    return jsonify({"message": "Location updated"}), 200
