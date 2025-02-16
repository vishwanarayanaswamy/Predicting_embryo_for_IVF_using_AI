from flask import Flask
from flask_cors import CORS
from config import Config
import routes  # Import entire routes module, not individual functions

import os

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# db.init_app(app)

# # Correct way to register routes
# app.add_url_rule('/register', view_func=routes.register_user, methods=['POST'])
# app.add_url_rule('/login', view_func=routes.login_user, methods=['POST'])
app.add_url_rule('/analyze', view_func=routes.analyze_embryo, methods=['POST'])

@app.route('/')
def home():
    return "Hello, Vishwa! Welcome to the IVF Embryo Analyzer API."


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Get port from environment or default to 5000
    app.run(host="0.0.0.0", port=port)
