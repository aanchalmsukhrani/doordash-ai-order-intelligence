<<<<<<< HEAD
# doordash-ai-order-intelligence
End-to-end AI project for a DoorDash-style food delivery platform: demand forecasting, customer insights, and API for integration.
=======
<<<<<<< HEAD
# doordash-ai-order-intelligence
End-to-end AI project for a DoorDash-style food delivery platform: demand forecasting, customer insights, and API for integration.
=======
# Smart Delivery ETA & Delay Risk

An end-to-end AI product demo inspired by DoorDash. It predicts **delivery ETA** and **delay risk** for food delivery orders, exposes a **REST API** using FastAPI, and includes a **Streamlit UI** for simulation and storytelling.

## 1. Problem

Customers lose trust when delivery ETAs are inaccurate. Support volume increases when orders are late with no proactive communication. This project demonstrates how an AI system can provide more realistic ETAs and early delay warnings.

## 2. Solution Overview

- **Synthetic dataset** mimicking food delivery orders
- **Regression model** predicting `actual_delivery_time_min`
- **Classification model** predicting `is_late` (late > 10 minutes)
- **FastAPI** service exposing `POST /predict-eta`
- **Streamlit** UI for interactive demos

## 3. Tech Stack

- Python, Pandas, NumPy
- scikit-learn, GradientBoosting models
- FastAPI, Uvicorn
- Streamlit
- joblib for model persistence

## 4. Running locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1) Generate data
cd data
python generate_synthetic_data.py
cd ..

# 2) Train models
python src/model/train_model.py

# 3) Start API
uvicorn src.api.main:app --reload --port 8000

# 4) In another terminal, start Streamlit
streamlit run app/streamlit_app.py
>>>>>>> 6a4115c4 (feat: initial DoorDash AI project setup)
>>>>>>> 3c64831 (feat: initial DoorDash AI project setup)
