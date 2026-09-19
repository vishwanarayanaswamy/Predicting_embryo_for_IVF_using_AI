# 🧬 IVF Embryo Analyzer – AI-Assisted Embryo Image Analysis

A full-stack web application that analyses an uploaded embryo image with two deep-learning models and reports whether the embryo looks **Healthy** or **Unhealthy**, together with a confidence score. Built with **TensorFlow/Keras**, a **Flask** REST API and a **React** front end.

> ⚠️ **Disclaimer:** This is an academic / educational project. It has **not been clinically validated** and must **not** be used for medical decisions, embryo selection or any real IVF treatment.

---

## ✨ Features

- 📤 Upload an embryo image and get a result in seconds
- 🔍 **Two-stage check:** first verifies that the image really is an embryo, then classifies its health
- 📊 Shows the prediction with a confidence value
- 🔐 User registration and login (passwords stored as salted hashes)
- 🗄 SQL database (MySQL or SQLite) with user and analysis tables
- 🖥 Simple, responsive React interface

---

## 🧠 How It Works

```mermaid
flowchart LR
    A[Upload image] --> B[Resize to 128×128<br/>scale to 0–1]
    B --> C{Embryo detector<br/>MobileNetV2}
    C -- "score < 0.5" --> D[Not an Embryo]
    C -- "score ≥ 0.5" --> E{Health classifier<br/>Xception}
    E -- "score ≥ 0.6" --> F[Healthy]
    E -- "score < 0.6" --> G[Unhealthy]
```

| Stage | Model | Purpose | Key settings |
|---|---|---|---|
| 1. Detector | MobileNetV2 (ImageNet weights) | Rejects images that are not embryos | Last 10 layers fine-tuned · Dense(256) + Dropout(0.5) · sigmoid output · Adam (lr 1e-4) · 20 epochs · data augmentation |
| 2. Classifier | Xception (ImageNet weights) | Healthy vs. Unhealthy | Last 10 layers fine-tuned · Dense(512) + Dropout(0.5) · sigmoid output · Adam (lr 1e-4) |

Both models take **128 × 128 RGB** images and are stored as `.h5` files (`embryo_detector.h5`, `xception_model.h5`).

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Deep learning | TensorFlow / Keras, OpenCV |
| Backend | Flask, Flask-CORS, Flask-SQLAlchemy |
| Database | MySQL (via PyMySQL) or SQLite |
| Frontend | React 19, React Router, Axios |

---

## 🗂 Project Structure

```
.
├── app.py                     # Flask app: creates the DB tables and registers routes
├── routes.py                  # /register, /login, /analyze endpoints + model inference
├── models.py                  # Database models: User, EmbryoAnalysis
├── db.py                      # SQLAlchemy setup and app factory
├── config.py                  # Configuration (reads environment variables)
├── xception.py                # Builds the Xception classifier architecture
├── train_embryo_detector.py   # Trains the embryo / non-embryo detector
├── download_images.py         # Helper to collect images for the detector dataset
├── embryo_detector.h5         # Trained detector (Git LFS)
├── xception_model.h5          # Trained classifier (Git LFS)
├── uploads/                   # Sample embryo images for testing
├── requirements.txt
├── frontend/                  # React app
│   └── src/
│       ├── App.js                 # Routes (login-protected)
│       ├── embrioAnalyser.jsx     # Upload + result page
│       └── components/            # Login.js, Register.js
└── LICENSE
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 – 3.12
- Node.js 18+ and npm
- [Git LFS](https://git-lfs.com) (the two `.h5` model files are stored with Git LFS)
- *(Optional)* MySQL 8 – without it the app uses a local SQLite file

### 1. Clone the repository

```bash
git lfs install
git clone https://github.com/vishwanarayanaswamy/Predicting_embryo_for_IVF_using_AI.git
cd Predicting_embryo_for_IVF_using_AI
git lfs pull        # makes sure the model files are downloaded
```

> If `xception_model.h5` and `embryo_detector.h5` are only ~130 bytes, Git LFS was not installed when you cloned – run `git lfs pull`.

### 2. Start the backend

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API runs at **http://127.0.0.1:5000**.

**Configuration (environment variables)**

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///ivf.db` | Database connection string, e.g. `mysql+pymysql://user:password@localhost/ivf_db` |
| `SECRET_KEY` | `dev-only-change-me` | Flask secret key – set your own value for anything beyond local testing |

For MySQL, create the database first (`CREATE DATABASE ivf_db;`) and set `DATABASE_URL` before starting the app. Never commit real passwords or keys to the repository.

### 3. Start the frontend

```bash
cd frontend
npm install
npm start
```

Open **http://localhost:3000**, register an account, log in and upload an image (sample images are in `uploads/`).

---

## 🔌 API Reference

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `GET` | `/` | – | Health check |
| `POST` | `/register` | JSON: `first_name`, `last_name`, `email`, `contact_number`, `address`, `username`, `password` | Create an account |
| `POST` | `/login` | JSON: `username`, `password` | Log in |
| `POST` | `/analyze` | multipart form: `image` | Analyse an embryo image |

**Example – analyse an image**

```bash
curl -X POST http://127.0.0.1:5000/analyze -F "image=@uploads/em.jpeg"
```

```json
{ "prediction": "Healthy", "confidence": 0.87 }
```

Possible `prediction` values: `Healthy`, `Unhealthy`, `Not an Embryo` (confidence `0.0`).

---

## 🏋️ Training the Models

**Embryo detector** (MobileNetV2)

1. Create the dataset folders:
   ```
   dataset/train/embryo/        # embryo images
   dataset/train/non_embryo/    # anything else: objects, animals, landscapes…
   ```
2. Run `python train_embryo_detector.py` – it saves `embryo_detector.h5`.

**Health classifier** (Xception)

`xception.py` defines the model architecture. The labelled healthy / unhealthy dataset and the training script for this model are not part of the repository.

---


---

## 🔮 Future Improvements

- Publish evaluation metrics (accuracy, precision, recall, ROC-AUC) and confusion matrices
- Add the training pipeline for the health classifier and document the dataset and its licence
- Real token-based authentication (JWT) and a protected `/analyze` route
- Save each analysis to the database and show a history page
- Explainability, e.g. Grad-CAM heat-maps on the embryo image
- Move the API URL to an environment variable and deploy backend and frontend

---

## 📄 License

Released under the [MIT License](LICENSE).

## 👤 Author

**Vishwa Narayanaswamy**
MSc Data Science, University of Europe for Applied Sciences
GitHub: [@vishwanarayanaswamy](https://github.com/vishwanarayanaswamy)
