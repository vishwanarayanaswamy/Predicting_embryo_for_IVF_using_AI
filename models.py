from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Ensure email is unique
    contact_number = db.Column(db.String(20), unique=True, nullable=False)  # Ensure contact number is unique
    address = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class EmbryoAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
