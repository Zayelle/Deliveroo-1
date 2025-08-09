from flask import Blueprint
from app.routes.auth_routes import auth_bp
from app.routes.parcel_routes import parcel_bp
from app.routes.admin_routes import admin_bp
from app.routes.user_routes import user_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(parcel_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
