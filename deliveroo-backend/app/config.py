from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()


migrate = Migrate()

# Base config class
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Optional if you're using JWT
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # Default: 1 hour
