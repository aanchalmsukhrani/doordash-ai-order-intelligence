import joblib
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL_DIR = HERE.parent / "model"

ETA_MODEL_PATH = MODEL_DIR / "eta_regressor.pkl"
DELAY_MODEL_PATH = MODEL_DIR / "delay_classifier.pkl"


class EtaModelService:
    def __init__(self):
        self.eta_model = joblib.load(ETA_MODEL_PATH)
        self.delay_model = joblib.load(DELAY_MODEL_PATH)

    def predict(self, features: dict):
        """
        features: dict with keys:
          distance_km, prep_time_min, estimated_travel_time_min,
          hour_of_day, day_of_week, is_raining, courier_experience
        """
        cols = [
            "distance_km",
            "prep_time_min",
            "estimated_travel_time_min",
            "hour_of_day",
            "day_of_week",
            "is_raining",
            "courier_experience",
        ]

        x = np.array([[features[c] for c in cols]], dtype=float)

        eta_pred = float(self.eta_model.predict(x)[0])

        delay_proba = float(self.delay_model.predict_proba(x)[0][1])

        risk_tag = "high_delay_risk" if delay_proba >= 0.5 else "on_time_likely"

        return eta_pred, delay_proba, risk_tag
