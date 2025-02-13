import os  # ✅ Make sure 'os' is imported
from flask import request, jsonify
import cv2
import numpy as np
import tensorflow as tf
import traceback  # For debugging

# 🔹 Load Models
MODEL_PATH = "xception_model.h5"
EMBRYO_DETECTOR_PATH = "embryo_detector.h5"

if not os.path.exists(MODEL_PATH) or not os.path.exists(EMBRYO_DETECTOR_PATH):
    print("❌ Model files missing! Ensure both models are trained.")
    exit()

model = tf.keras.models.load_model(MODEL_PATH)
embryo_detector = tf.keras.models.load_model(EMBRYO_DETECTOR_PATH)

# 🔹 Helper Function: Preprocess Image
def preprocess_image(image):
    npimg = np.frombuffer(image.read(), np.uint8)  # Convert file to numpy array
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)  # Decode image
    img = cv2.resize(img, (128, 128))  # Resize to match model input
    img = img / 255.0  # Normalize pixel values (scale between 0 and 1)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# 🔹 Basic Embryo Analysis API (No Database)
def analyze_embryo():
    try:
        # ✅ Ensure an image is uploaded
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]
        processed_image = preprocess_image(image)

        # ✅ Step 1: Check if the image is an embryo
        embryo_prediction = embryo_detector.predict(processed_image)
        is_embryo = embryo_prediction[0][0] >= 0.5  # 1 = Embryo, 0 = Not Embryo
        print("Is Embryo:", is_embryo)

        if not is_embryo:
            return jsonify({"prediction": "Not an Embryo", "confidence": 0.0})

        # ✅ Step 2: Classify as Healthy/Unhealthy using Xception model
        predictions = model.predict(processed_image)
        confidence = float(predictions[0][0])

        predicted_class = "Healthy" if confidence >= 0.5 else "Unhealthy"

        return jsonify({"prediction": predicted_class, "confidence": round(confidence, 2)})

    except Exception as e:
        print("❌ Error in analyze_embryo:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Something went wrong!", "details": str(e)}), 500
