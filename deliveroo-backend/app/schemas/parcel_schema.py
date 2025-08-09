from app import ma
from app.models.parcel import Parcel

class ParcelSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Parcel
        load_instance = True
        ordered = True

    id = ma.auto_field()
    sender_id = ma.auto_field()
    recipient = ma.auto_field()
    destination = ma.auto_field()
    present_location = ma.auto_field()
    status_id = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
