from app.presenters.auth_presenter import register_user, login_user
from flask import request

def register_user_controller():
    data = request.get_json()
    return register_user(data)

def login_user_controller():
    data = request.get_json()
    return login_user(data)

