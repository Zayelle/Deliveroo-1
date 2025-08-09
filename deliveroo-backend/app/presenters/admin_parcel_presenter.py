import logging
from flask import jsonify
from app.models.parcel import Parcel
from app.models.user import User
from app.extensions import db

from marshmallow import Schema, fields, ValidationError

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VALID_STATUSES = ["Pending", "In Transit", "Delivered", "Cancelled"]

# Marshmallow Schemas
class StatusUpdateSchema(Schema):
    status = fields.String(required=True)

class LocationUpdateSchema(Schema):
    current_location = fields.String(required=True)

class BulkParcelSchema(Schema):
    parcel_id = fields.Int(required=True)
    status = fields.String(validate=lambda s: s in VALID_STATUSES)
    current_location = fields.String()

# Helpers
def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.is_admin


# ============================
# Single Parcel Status Update
# ============================
def update_parcel_status(admin_id, parcel_id, data):
    if not is_admin(admin_id):
        logger.warning(f"Unauthorized status update attempt by user {admin_id}")
        return jsonify({"status": "error", "message": "Admin access required."}), 403

    try:
        validated = StatusUpdateSchema().load(data)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({"status": "error", "message": err.messages}), 400

    parcel = Parcel.query.get(parcel_id)
    if not parcel:
        logger.info(f"Parcel ID {parcel_id} not found for status update.")
        return jsonify({"status": "error", "message": "Parcel not found."}), 404

    parcel.status = validated["status"]
    db.session.commit()

    logger.info(f"Parcel ID {parcel_id} status updated to {validated['status']}")
    return jsonify({
        "status": "success",
        "message": f"Parcel status updated to '{parcel.status}'.",
        "data": {"parcel_id": parcel.id, "status": parcel.status}
    }), 200


# ===============================
# Single Parcel Location Update
# ===============================
def update_parcel_location(admin_id, parcel_id, data):
    if not is_admin(admin_id):
        logger.warning(f"Unauthorized location update attempt by user {admin_id}")
        return jsonify({"status": "error", "message": "Admin access required."}), 403

    try:
        validated = LocationUpdateSchema().load(data)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({"status": "error", "message": err.messages}), 400

    parcel = Parcel.query.get(parcel_id)
    if not parcel:
        logger.info(f"Parcel ID {parcel_id} not found for location update.")
        return jsonify({"status": "error", "message": "Parcel not found."}), 404

    parcel.current_location = validated["current_location"]
    db.session.commit()

    logger.info(f"Parcel ID {parcel_id} location updated to {validated['current_location']}")
    return jsonify({
        "status": "success",
        "message": "Parcel location updated.",
        "data": {"parcel_id": parcel.id, "current_location": parcel.current_location}
    }), 200


# ==========================
# Bulk Update Status/Location
# ==========================
def bulk_update_parcels(admin_id, parcels_data):
    if not is_admin(admin_id):
        logger.warning(f"Unauthorized bulk update attempt by user {admin_id}")
        return jsonify({"status": "error", "message": "Admin access required."}), 403

    schema = BulkParcelSchema(many=True)
    try:
        validated_data = schema.load(parcels_data)
    except ValidationError as err:
        logger.error(f"Bulk validation error: {err.messages}")
        return jsonify({"status": "error", "message": err.messages}), 400

    results = []

    for entry in validated_data:
        parcel = Parcel.query.get(entry["parcel_id"])
        if not parcel:
            logger.warning(f"Parcel ID {entry['parcel_id']} not found in bulk update.")
            results.append({
                "parcel_id": entry["parcel_id"],
                "status": "failed",
                "message": "Parcel not found."
            })
            continue

        if "status" in entry:
            parcel.status = entry["status"]
        if "current_location" in entry:
            parcel.current_location = entry["current_location"]

        results.append({
            "parcel_id": parcel.id,
            "status": "success",
            "new_status": parcel.status,
            "current_location": parcel.current_location
        })

    db.session.commit()
    logger.info(f"Bulk update performed on {len(results)} parcels.")

    return jsonify({
        "status": "success",
        "message": f"{len(results)} parcels updated.",
        "results": results
    }), 200
