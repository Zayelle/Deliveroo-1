from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.parcel import Parcel
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.parcel_schema import DestinationUpdateSchema
from app.schemas.user_schema import UserDeleteSchema

def get_user_parcels():
    user_id = get_jwt_identity()["id"]
    parcels = Parcel.query.filter_by(user_id=user_id).all()
    return jsonify([parcel.to_dict() for parcel in parcels]), 200

def get_user_parcel(parcel_id):
    user_id = get_jwt_identity()["id"]
    parcel = Parcel.query.filter_by(id=parcel_id, user_id=user_id).first()
    if not parcel:
        return jsonify({"error": "Parcel not found"}), 404
    return jsonify(parcel.to_dict()), 200

def cancel_parcel(parcel_id):
    user_id = get_jwt_identity()["id"]
    parcel = Parcel.query.filter_by(id=parcel_id, user_id=user_id).first()

    if not parcel:
        return jsonify({"error": "Parcel not found"}), 404
    if parcel.status.lower() in ["cancelled","delivered"]:
        return jsonify({"error": f"Cannot cancel a {parcel.status.lower()}parcel"}), 400

    parcel.status = "Cancelled"
    db.session.commit()
    return jsonify({"message": "Parcel cancelled successfully"}), 200

def update_parcel_destination(parcel_id, data):
    user_id = get_jwt_identity()["id"]
    parcel = Parcel.query.filter_by(id=parcel_id, user_id=user_id).first()

    if not parcel:
        return jsonify({"error": "Parcel not found"}), 404
    if parcel.status.lower() == "delivered":
        return jsonify({"error": "Cannot update destination of a delivered parcel"}), 400

    # Input validation
    errors = DestinationUpdateSchema().validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    parcel.destination = data["destination"]
    db.session.commit()
    return jsonify({"message": "Destination updated successfully"}), 200

def delete_user_account(requester_id, target_user_id, data=None):
    requester = User.query.get(requester_id)
    user = User.query.get(target_user_id)

    if not user or user.is_deleted:
        return jsonify({"error": "User not found or already deleted"}), 404

    # Only allow if user is admin or deleting their own account
    if not (requester.is_admin or requester_id == target_user_id):
        return jsonify({"error": "Unauthorized"}), 403

    # If user is NOT admin, require password validation
    if not requester.is_admin:
        if not data:
            return jsonify({"error": "Password required"}), 400
        errors = UserDeleteSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400
        if not user.check_password(data["password"]):
            return jsonify({"error": "Incorrect password"}), 403

    try:
        user.is_deleted = True
        db.session.commit()
        return jsonify({"status": "success", "message": "User account deleted"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
