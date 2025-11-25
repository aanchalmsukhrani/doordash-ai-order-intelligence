import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.metrics import mean_absolute_error, r2_score, classification_report

DATA_PATH = "data/synthetic_orders.csv"
ETA_MODEL_PATH = "src/model/eta_regressor.pkl"
DELAY_MODEL_PATH = "src/model/delay_classifier.pkl"


def load_data(path: str):
    df = pd.read_csv(path)

    feature_cols = [
        "distance_km",
        "prep_time_min",
        "estimated_travel_time_min",
        "hour_of_day",
        "day_of_week",
        "is_raining",
        "courier_experience",
    ]

    X = df[feature_cols]
    y_eta = df["actual_delivery_time_min"]
    y_delay = df["is_late"]

    return X, y_eta, y_delay


def train_eta_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("ETA Regression MAE:", mae)
    print("ETA Regression R^2:", r2)
    return model


def train_delay_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Delay Classification Report:")
    print(classification_report(y_test, y_pred))

    return model


def main():
    print("Loading data from", DATA_PATH)
    X, y_eta, y_delay = load_data(DATA_PATH)

    print("\nTraining ETA model...")
    eta_model = train_eta_model(X, y_eta)
    joblib.dump(eta_model, ETA_MODEL_PATH)
    print("Saved ETA model to", ETA_MODEL_PATH)

    print("\nTraining delay model...")
    delay_model = train_delay_model(X, y_delay)
    joblib.dump(delay_model, DELAY_MODEL_PATH)
    print("Saved delay model to", DELAY_MODEL_PATH)


if __name__ == "__main__":
    main()
