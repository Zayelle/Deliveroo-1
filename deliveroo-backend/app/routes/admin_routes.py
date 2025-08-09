from flask import Blueprint, request, jsonify
from app.models.parcel import Parcel
from app.models.user import User
from app.extensions import db

from app.utils.decorators import admin_required

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/parcels/<int:id>', methods=['PATCH'])
@admin_required
def admin_update_parcel(id):
    data = request.get_json()
    parcel = Parcel.query.get_or_404(id)

    if 'status_id' in data:
        parcel.status_id = data['status_id']
    if 'destination' in data:
        parcel.destination = data['destination']
    if 'present_location' in data:
        parcel.present_location = data['present_location']

    db.session.commit()
    return jsonify(parcel.to_dict()), 200

@admin_bp.route('/assign-role', methods=['POST'])
@admin_required
def assign_role():
    data = request.get_json()
    user_id = data.get('user_id')
    role = data.get('role')

    if not user_id or not role:
        return jsonify({"error": "Missing user_id or role"}), 400

    if role.lower() not in ['user', 'admin']:
        return jsonify({"error": "Invalid role"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.role = role.lower()
    db.session.commit()
    return jsonify(user.to_dict()), 200

@admin_bp.route('/parcels', methods=['GET'])
@admin_required
def get_all_parcels():
    parcels = Parcel.query.all()
    return jsonify([parcel.to_dict() for parcel in parcels]), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    role = request.args.get('role')
    if role:
        users = User.query.filter(User.role.ilike(role)).all()
    else:
        users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200



