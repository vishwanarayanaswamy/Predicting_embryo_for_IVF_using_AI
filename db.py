from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)  # ✅ Bind SQLAlchemy to the app

    with app.app_context():
        db.create_all()  # ✅ Ensure database tables are created

    return app  # ✅ Return the initialized Flask app
