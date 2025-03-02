import os
import traceback
import cv2
import numpy as np
import tensorflow as tf
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import db  # ✅ Import db directly to avoid circular import issues
from models import User  # ✅ Ensure User model is properly defined

# 🔹 Model Paths
MODEL_PATH = "xception_model.h5"
EMBRYO_DETECTOR_PATH = "embryo_detector.h5"

# 🔹 Lazy Load Models
model = None
embryo_detector = None

def load_models():
    global model, embryo_detector
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH)
        else:
            print("❌ Error: Missing classification model!")

    if embryo_detector is None:
        if os.path.exists(EMBRYO_DETECTOR_PATH):
            embryo_detector = tf.keras.models.load_model(EMBRYO_DETECTOR_PATH)
        else:
            print("❌ Error: Missing embryo detection model!")

# 🔹 Image Preprocessing
def preprocess_image(image):
    npimg = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# 🔹 Analyze Embryo API
def analyze_embryo():
    try:
        load_models()  # ✅ Ensure models are loaded

        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]
        processed_image = preprocess_image(image)

        # ✅ Step 1: Check if image is an embryo
        embryo_prediction = embryo_detector.predict(processed_image)
        is_embryo = embryo_prediction[0][0] >= 0.5

        if not is_embryo:
            return jsonify({"prediction": "Not an Embryo", "confidence": 0.0})

        # ✅ Step 2: Classify as Healthy/Unhealthy
        predictions = model.predict(processed_image)
        confidence = float(predictions[0][0])
        predicted_class = "Healthy" if confidence >= 0.6 else "Unhealthy"

        return jsonify({"prediction": predicted_class, "confidence": round(confidence, 2)})

    except Exception as e:
        print("❌ Error in analyze_embryo:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Something went wrong!", "details": str(e)}), 500

# 🔹 Register User API
def register_user():
    try:
        data = request.json
        print(data, "datasss")
        if not data or not all(k in data for k in ["first_name", "last_name", "id", "email", "address", "contact_number", "username", "password"]):
            return jsonify({"error": "Missing required fields"}), 400

        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already exists"}), 409

        hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            id=data["id"],
            email=data["email"],
            address=data["address"],
            contact_number=data["contact_number"],
            username=data["username"],
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully","success":"true","token":"testinggg"}), 201

    except Exception as e:
        print("❌ Error in register_user:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Something went wrong!", "details": str(e)}), 500

# 🔹 Login User API
def login_user():
    try:
        data = request.json
        if not data or not all(k in data for k in ["username", "password"]):
            return jsonify({"error": "Missing required fields"}), 400

        user = User.query.filter_by(username=data["username"]).first()

        if user and check_password_hash(user.password, data["password"]):
            print("success")
            return jsonify({"message": "Login successful","success":"true","token":"testinggg"}), 200

        return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print("❌ Error in login_user:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Something went wrong!", "details": str(e)}), 500
