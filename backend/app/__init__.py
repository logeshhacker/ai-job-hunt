# Flask app factory with SQLAlchemy, JWT, CORS configuration using environment variables
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name='development'):
    """
    Application factory function that creates and configures the Flask app.
    
    Args:
        config_name: Configuration environment ('development', 'testing', 'production')
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///app.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv(
        'JWT_SECRET_KEY',
        'dev-secret-key-change-in-production'
    )
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(
        os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)
    )
    
    # CORS Configuration
    cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS(app, resources={r'/api/*': {'origins': cors_origins}})
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    
    # Create database tables
    with app.app_context():
        from app.models.user import User

        db.create_all()
    
    # Register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app