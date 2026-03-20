"""
WSGI entry point for the Flask application.
Initializes the app and prepares it for production deployment.
"""
import os
from app import create_app, db

# Create the Flask application instance
app = create_app(config_name=os.getenv('FLASK_ENV', 'development'))

# Create all database tables on startup
with app.app_context():
    db.create_all()

# Enable debug mode if in development environment
debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'

if __name__ == '__main__':
    app.run(debug=debug_mode)
