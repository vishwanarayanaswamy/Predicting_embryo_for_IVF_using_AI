from flask import request, jsonify
from models import db, User
import bcrypt
import jwt
import datetime
import os
import cv2
import numpy as np
import tensorflow as tf

# 🔹 Load Models
MODEL_PATH = "xception_model.h5"
EMBRYO_DETECTOR_PATH = "embryo_detector.h5"

if not os.path.exists(MODEL_PATH) or not os.path.exists(EMBRYO_DETECTOR_PATH):
    print("❌ Model files missing! Ensure both models are trained.")
    exit()

model = tf.keras.models.load_model(MODEL_PATH)
embryo_detector = tf.keras.models.load_model(EMBRYO_DETECTOR_PATH)

# 🔹 Ensure 'uploads/' folder exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔹 Helper Function: Preprocess Image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (128, 128))  # Resize to match model input
    img = img / 255.0  # Normalize pixel values (scale between 0 and 1)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# 🔹 Register User (Auto Login)
def register_user():
    data = request.get_json()

    # Check if email exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already exists!'}), 400

    # Check if contact number exists
    existing_contact = User.query.filter_by(contact_number=data['contact_number']).first()
    if existing_contact:
        return jsonify({'error': 'Contact number already exists!'}), 400

    # Hash password before storing
    hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

    # Store user in database
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        contact_number=data['contact_number'],
        address=data['address'],
        username=data['username'],
        password=hashed_password.decode()  # Store hashed password as string
    )

    db.session.add(new_user)
    db.session.commit()

    # ✅ Auto-login after registration
    token = jwt.encode({'user_id': new_user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 
                       "your_secret_key", algorithm='HS256')

    return jsonify({'message': 'User registered successfully!', 'token': token})

# 🔹 Login User
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({'error': 'User not found'}), 401

    # Debugging logs
    print(f"🔹 User Found: {user.username}")
    print(f"🔹 Input Password: {data['password']}")
    print(f"🔹 Stored Password (Hashed): {user.password}")

    # ✅ Ensure correct password verification
    if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 
                           "your_secret_key", algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 401

# 🔹 Embryo Analysis API (JWT Protected)
import traceback  # ✅ Import for better debugging

def analyze_embryo():
    try:
        # ✅ Ensure JWT Token is provided
      
      
        # ✅ Ensure an image is uploaded
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]

        # ✅ Ensure absolute path & save image
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        processed_image = preprocess_image(image_path)

        # ✅ Step 1: Check if the image is an embryo
        embryo_prediction = embryo_detector.predict(processed_image)
        is_embryo = embryo_prediction[0][0] >= 0.5  # 1 = Embryo, 0 = Not Embryo
        print(is_embryo)
        if not is_embryo:
            return jsonify({"prediction": "Unhealthy", "confidence": 0.0})

        # ✅ Step 2: Classify as Healthy/Unhealthy using Xception model
        predictions = model.predict(processed_image)
        confidence = float(predictions[0][0])

        predicted_class = "Healthy" if confidence >= 0.5 else "Unhealthy"

        return jsonify({"prediction": predicted_class, "confidence": round(confidence, 2)})

    except Exception as e:
        print("❌ Error in analyze_embryo:", str(e))
        traceback.print_exc()  # ✅ Show full error traceback in logs
        return jsonify({"error": "Something went wrong!", "details": str(e)}), 500