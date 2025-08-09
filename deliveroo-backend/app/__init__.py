from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from .config import Config
from app.extensions import db, migrate, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=[ "http://localhost:8080"], supports_credentials=True)

    # Health & Debug Routes
    @app.route("/", methods=["GET"])
    def root():
        return "Deliveroo API is live. Use /index for info."

    @app.route("/index", methods=["GET"])
    def index():
        return {"message": "Welcome to the Deliveroo API!"}

    @app.route("/profile", methods=["GET"])
    @jwt_required()
    def profile():
        current_user = get_jwt_identity()
        return jsonify(current_user), 200

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.parcel_routes import parcel_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.email_routes import email_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(parcel_bp, url_prefix="/parcels")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(email_bp, url_prefix="/email")  

    return app

# Expose app factory and extensions
__all__ = ["create_app", "db", "migrate", "jwt"]