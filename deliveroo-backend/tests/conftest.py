import pytest
from app import create_app, db
from app.models import Location, Status

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seed_data(app):
    """Seed initial data like locations and statuses (no Role)."""
    location1 = Location(name="Nairobi")
    location2 = Location(name="Mombasa")
    pending_status = Status(name="Pending")
    delivered_status = Status(name="Delivered")

    db.session.add_all([location1, location2, pending_status, delivered_status])
    db.session.commit()
