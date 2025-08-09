from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.extensions import db


def get_all_users():
    """
    Retrieve all users from the database.
    """
    users = User.query.all()
    users_data = [{
        "id": user.id,
        "username": user.name
,
        "email": user.email,
        "is_admin": user.is_admin
    } for user in users]

    return jsonify({
        "status": "success",
        "data": users_data
    }), 200

def promote_user(user_id):
    """
    Promote a user to admin.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    if user.is_admin:
        return jsonify({"status": "error", "message": "User is already an admin."}), 400

    user.is_admin = True
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": f"User '{user.name}' promoted to admin."
    }), 200

def demote_user(user_id):
    """
    Demote an admin to a regular user.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    current_user_id = get_jwt_identity()
    if user.id == current_user_id:
        return jsonify({"status": "error", "message": "You cannot demote yourself."}), 403

    if not user.is_admin:
        return jsonify({"status": "error", "message": "User is not an admin."}), 400

    user.is_admin = False
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": f"User '{user.name}' demoted from admin."
    }), 200

def delete_user(user_id):
    """
    Soft delete a user account.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    current_user_id = get_jwt_identity()
    if user.id == current_user_id:
        return jsonify({"status": "error", "message": "You cannot delete your own account."}), 403

    user.is_deleted = True
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": f"User '{user.name}' has been  soft-deleted."
    }), 200

