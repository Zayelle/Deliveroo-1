from flask import request
from app.presenters.admin_presenter import (
    get_all_users,
    promote_user,
    demote_user,
    delete_user
)

def get_all_users_controller():
    return get_all_users()

def promote_user_controller(user_id):
    return promote_user(user_id)

def demote_user_controller(user_id):
    return demote_user(user_id)

def delete_user_controller(user_id):
    return delete_user(user_id)
