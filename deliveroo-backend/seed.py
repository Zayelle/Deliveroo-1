from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.location import Location
from app.models.parcel import Parcel
from app.models.status import Status
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

def seed_data():
    db.drop_all()
    db.create_all()

      # Prevent reseeding if users already exist
    if User.query.first():
        print("⚠️ Database already seeded. Aborting.")
        return

    # Seed Users (active and soft-deleted)
    users = [
        User(name="Alice Smith", email="alice@example.com", role="admin", password_hash=generate_password_hash("password")),
        User(name="Bob Johnson", email="bob@example.com", role="courier", password_hash=generate_password_hash("password")),
        User(name="Carol Lee", email="carol@example.com", role="user", password_hash=generate_password_hash("password")),

        # Soft-deleted users
        User(name="Deleted Admin", email="del_admin@example.com", role="admin", password_hash=generate_password_hash("password"), is_deleted=True),
        User(name="Deleted Courier", email="del_courier@example.com", role="courier", password_hash=generate_password_hash("password"), is_deleted=True),
        User(name="Deleted User", email="del_user@example.com", role="user", password_hash=generate_password_hash("password"), is_deleted=True),
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()

    # Seed Locations
    locations = [
        Location(city="Nairobi", address="Kenyatta Avenue"),
        Location(city="Mombasa", address="Moi Avenue"),
        Location(city="Kisumu", address="Oginga Odinga St"),
    ]
    db.session.add_all(locations)
    db.session.commit()

    # Seed Statuses
    statuses = [
        Status(name="Pending"),
        Status(name="In Transit"),
        Status(name="Delivered"),
        Status(name="Cancelled")
    ]
    db.session.add_all(statuses)
    db.session.commit()

    # Seed Parcels (only for active users)
    active_users = User.query.filter_by(is_deleted=False).all()
    parcels = [
        Parcel(
            description="Electronics",
            user_id=active_users[2].id,
            origin=locations[0].id,
            destination=locations[1].id,
            status_id=statuses[0].id,
            created_at=datetime.utcnow()
        ),
        Parcel(
            description="Books",
            user_id=active_users[2].id,
            origin=locations[1].id,
            destination=locations[2].id,
            status_id=statuses[1].id,
            created_at=datetime.utcnow()
        )
    ]
    db.session.add_all(parcels)
    db.session.commit()

    print("✅ Database seeded with users (including soft-deleted), locations, statuses, and parcels.")

if __name__ == "__main__":
    with app.app_context():
        print("🌱 Seeding database...")
        seed_data()
