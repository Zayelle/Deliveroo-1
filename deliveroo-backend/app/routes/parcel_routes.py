from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.parcel import Parcel
from app.models.user import User
from app.extensions import db


parcel_bp = Blueprint('parcel_bp', __name__, url_prefix='/parcels')

@parcel_bp.route('', methods=['GET'])
@jwt_required()
def get_parcels():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.role == 'admin':
        parcels = Parcel.query.all()
    else:
        parcels = Parcel.query.filter_by(user_id=current_user_id).all()
    return jsonify([parcel.to_dict() for parcel in parcels]), 200

@parcel_bp.route('', methods=['POST'])
@jwt_required()
def create_parcel():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    parcel = Parcel(
        weight=data['weight'],
        pickup_location=data['pickup_location'],
        destination=data['destination'],
        user_id=current_user_id
    )
    db.session.add(parcel)
    db.session.commit()
    return jsonify(parcel.to_dict()), 201

@parcel_bp.route('/<int:parcel_id>', methods=['GET'])
@jwt_required()
def get_parcel(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    return jsonify(parcel.to_dict()), 200

@parcel_bp.route('/<int:parcel_id>', methods=['PATCH'])
@jwt_required()
def update_parcel(parcel_id):
    data = request.get_json()
    parcel = Parcel.query.get_or_404(parcel_id)
    current_user_id = get_jwt_identity()
    if parcel.user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
      # ❌ Prevent editing delivered parcels
    if parcel.status.lower() == 'delivered':
        return jsonify({"error": "Cannot update a delivered parcel"}), 400
    
      # ✅ Allow destination update only
    if 'destination' in data:
        parcel.destination = data['destination']
        db.session.commit()
        return jsonify(parcel.to_dict()), 200
    else:
        return jsonify({"error": "Only destination can be updated"}), 400

@parcel_bp.route('/<int:parcel_id>', methods=['DELETE'])
@jwt_required()
def delete_parcel(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    current_user_id = get_jwt_identity()
    if parcel.user_id != current_user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
      # ❌ Prevent deleting delivered parcels
    if parcel.status.lower() == 'delivered':
        return jsonify({"error": "Cannot cancel a delivered parcel"}), 400

    db.session.delete(parcel)
    db.session.commit()
    return jsonify({"message": "Parcel cancelled successfully"}), 200
