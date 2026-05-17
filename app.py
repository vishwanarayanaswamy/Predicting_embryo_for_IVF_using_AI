from flask import Flask
from flask_cors import CORS
import routes  # Import routes after initializing the app
import os
from db import db, create_app  # ✅ Import create_app from db.py

app = create_app()  # ✅ Initialize Flask app
CORS(app)

# ✅ Drop all tables and recreate them
with app.app_context():
    try:
        ("⚠️ Dropping all existing tables...")
        db.drop_all()  # Deletes all tables
        print("✅ Creating new tables...")
        db.create_all()  # Creates fresh tables based on models
        print("🚀 Database reset complete!")
    except Exception as e:
        print("❌ Error resetting the database:", str(e))

# ✅ Register Routes
try:
    app.add_url_rule('/register', view_func=routes.register_user, methods=['POST'])
    app.add_url_rule('/login', view_func=routes.login_user, methods=['POST'])
except AttributeError:
    print("⚠️ Warning: 'register_user' or 'login_user' not found in routes.py.")

app.add_url_rule('/analyze', view_func=routes.analyze_embryo, methods=['POST'])

@app.route('/')
def home():
    return "Hello, Vishwa! Welcome to the IVF Embryo Analyzer API."

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
