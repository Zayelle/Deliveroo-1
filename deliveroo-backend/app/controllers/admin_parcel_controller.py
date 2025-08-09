from flask import request
from flask_jwt_extended import get_jwt_identity
from app.presenters.admin_parcel_presenter import (
    update_parcel_status,
    update_parcel_location,
    bulk_update_parcels
)

# PATCH /admin/parcels/<parcel_id>/status
def update_parcel_status_controller(parcel_id):
    data = request.get_json()
    admin_id = get_jwt_identity().get("id")
    return update_parcel_status(admin_id, parcel_id, data)

# PATCH /admin/parcels/<parcel_id>/location
def update_parcel_location_controller(parcel_id):
    data = request.get_json()
    admin_id = get_jwt_identity().get("id")
    return update_parcel_location(admin_id, parcel_id, data)

# PATCH /admin/parcels/bulk-update
def bulk_update_parcels_controller():
    data = request.get_json()
    admin_id = get_jwt_identity().get("id")
    return bulk_update_parcels(admin_id, data)

