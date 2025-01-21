from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


# Flask application setup
app = Flask(__name__)
app.secret_key = '@123789'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NiounNotary_requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# SQLAlchemy instance
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Import routes to register them with the app
from routes import *

# Database initialization with application context
def initialize_database():
    with app.app_context():
        db.create_all()

# Mock user database
users = {"admin": {"password": "password123"}}


# Main entry point

if __name__ == '__main__':
    initialize_database()  # Ensure tables are created before the server starts
    app.run(debug=True)

