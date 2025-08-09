from app import ma
from app.models.status import Status

class StatusSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Status
        load_instance = True
        ordered = True  # Ensures JSON output is ordered as fields are defined

    id = ma.auto_field()
    name = ma.auto_field(required=True)
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
