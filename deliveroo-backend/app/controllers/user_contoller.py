from flask import request
from flask_jwt_extended import get_jwt_identity
from app.presenters.user_presenter import (
    get_user_profile,
    update_user_profile,
    delete_user_account
)

def get_user_profile_controller():
    user_id = get_jwt_identity().get("id")
    return get_user_profile(user_id)

def update_user_profile_controller():
    user_id = get_jwt_identity().get("id")
    data = request.get_json()
    return update_user_profile(user_id, data)

def delete_user_account_controller():
    user_id = get_jwt_identity().get("id")
    data = request.get_json
    return delete_user_account(user_id,data)
