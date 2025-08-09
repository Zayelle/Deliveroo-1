from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.presenters.auth_presenter import register_user, login_user

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200

