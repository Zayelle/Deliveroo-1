from flask import request
from flask_jwt_extended import get_jwt_identity
from app.presenters.parcel_presenter import (
    create_parcel_order,
    get_user_parcels,
    get_parcel_by_id,
    update_parcel_destination,
    cancel_parcel_order
)

def create_parcel_controller():
    data = request.get_json()
    user_id = get_jwt_identity().get("id")
    return create_parcel_order(user_id, data)

def get_user_parcels_controller():
    user_id = get_jwt_identity().get("id")
    return get_user_parcels(user_id)

def get_parcel_by_id_controller(parcel_id):
    user_id = get_jwt_identity().get("id")
    return get_parcel_by_id(user_id, parcel_id)

def update_parcel_destination_controller(parcel_id):
    data = request.get_json()
    user_id = get_jwt_identity().get("id")
    return update_parcel_destination(user_id, parcel_id, data)

def cancel_parcel_controller(parcel_id):
    user_id = get_jwt_identity().get("id")
    return cancel_parcel_order(user_id, parcel_id)
