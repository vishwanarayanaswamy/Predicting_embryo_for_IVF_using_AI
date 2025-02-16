from flask import Flask
from flask_cors import CORS
#from models import db
from config import Config
import routes  # Import entire routes module, not individual functions

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
    app.run(debug=True)
