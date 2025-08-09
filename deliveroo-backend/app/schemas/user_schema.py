from app import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    is_deleted = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)

