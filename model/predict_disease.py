import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np


class DiseaseRiskModel:
    def __init__(self):
        self.shared_features = [
            "age", "sex", "bmi", "weight", "blood_pressure",
            "heart_rate", "smoking_status", "cholesterol", "glucose"
        ]
        self.model = None
        self.scaler = None
        self.load_model()

    def load_and_prepare_data(self):
        # Use your empirical dataset
        data = pd.read_csv("merged_healthdata.csv")

        target_columns = ["heart_disease_10yr_risk", "stroke_10yr_risk"]
        data = data[self.shared_features + target_columns].dropna()

        X = data[self.shared_features]
        y = data[target_columns]

        return X, y

    def train_and_save_model(self):
        X, y = self.load_and_prepare_data()

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = MultiOutputRegressor(
            RandomForestRegressor(random_state=42, n_estimators=100)
        )
        self.model.fit(X_scaled, y)

        joblib.dump(self.model, "multi_disease_regressor.pkl")
        joblib.dump(self.scaler, "scaler.pkl")

    def load_model(self):
        try:
            self.model = joblib.load("multi_disease_regressor.pkl")
            self.scaler = joblib.load("scaler.pkl")
        except FileNotFoundError:
            self.train_and_save_model()

    def predict(self, user_input):
        # Prepare input for ML model
        input_df = pd.DataFrame([user_input])[self.shared_features]
        input_scaled = self.scaler.transform(input_df)
        model_pred = self.model.predict(input_scaled)[0]

        # Formula-based risk estimation
        def calc_heart_disease_risk(features):
            risk = (
                0.0015 * (features["age"] - 20) +
                0.03 * features["sex"] +
                0.02 * (features["bmi"] - 22) +
                0.015 * (features["blood_pressure"] - 120) +
                0.02 * features["smoking_status"] +
                0.01 * ((features["cholesterol"] - 180) / 10) +
                0.015 * ((features["glucose"] - 90) / 10)
            )
            return np.clip(risk, 0, 1)

        def calc_stroke_risk(features):
            risk = (
                0.0017 * (features["age"] - 20) +
                0.025 * features["sex"] +
                0.017 * (features["bmi"] - 22) +
                0.02 * (features["blood_pressure"] - 120) +
                0.025 * features["smoking_status"] +
                0.012 * ((features["cholesterol"] - 180) / 10) +
                0.02 * ((features["glucose"] - 90) / 10)
            )
            return np.clip(risk, 0, 1)

        # Get formula predictions
        hd_formula = calc_heart_disease_risk(user_input)
        st_formula = calc_stroke_risk(user_input)

        # Combine ML and formula predictions
        hd_final = np.clip((model_pred[0] + hd_formula) / 2, 0, 1)
        st_final = np.clip((model_pred[1] + st_formula) / 2, 0, 1)

        return {
            "heart_disease_10yr_risk": float(hd_final),
            "stroke_10yr_risk": float(st_final)
        }


# Global instance
disease_model = DiseaseRiskModel()

def predict_diseases(user_input):
    return disease_model.predict(user_input)


# Uncomment for standalone test
# if __name__ == "__main__":
#     test_input = {
#         "age": 52,
#         "sex": 1,
#         "bmi": 27.5,
#         "weight": 82,
#         "blood_pressure": 138,
#         "heart_rate": 76,
#         "smoking_status": 1,
#         "cholesterol": 195,
#         "glucose": 100
#     }
#     result = predict_diseases(test_input)
#     print("10-Year Risk Prediction:")
#     print(f"Heart Disease Risk: {result['heart_disease_10yr_risk']:.3f}")
#     print(f"Stroke Risk: {result['stroke_10yr_risk']:.3f}")
