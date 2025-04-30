import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.utils import resample


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
        data = pd.read_csv("healthdata.csv")

        target_columns = ["has_heart_disease", "has_stroke"]
        data = data[self.shared_features + target_columns].dropna()

        X = data[self.shared_features]
        y = data[target_columns]

        return X, y


    def train_and_save_model(self):
        X, y = self.load_and_prepare_data()

        # Combine labels into a single string to stratify on label combinations
        combined = y.astype(str).agg('_'.join, axis=1)
        data = pd.concat([X, y], axis=1)
        data['label_combo'] = combined

        # Find the smallest class size to downsample to
        min_size = data['label_combo'].value_counts().min()

        # Undersample each group to match the smallest group size
        balanced_data = pd.concat([
            resample(group, replace=False, n_samples=min_size, random_state=42)
            for _, group in data.groupby('label_combo')
        ])

        X_balanced = balanced_data[self.shared_features]
        y_balanced = balanced_data[["has_heart_disease", "has_stroke"]]

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_balanced)

        self.model = MultiOutputClassifier(RandomForestClassifier(random_state=42))
        self.model.fit(X_scaled, y_balanced)

        joblib.dump(self.model, "multi_disease_model.pkl")
        joblib.dump(self.scaler, "scaler.pkl")


    def load_model(self):
        try:
            self.model = joblib.load("multi_disease_model.pkl")
            self.scaler = joblib.load("scaler.pkl")
        except FileNotFoundError:
            self.train_and_save_model()

    def predict(self, user_input):
        input_df = pd.DataFrame([user_input])
        input_scaled = self.scaler.transform(input_df[self.shared_features])
        predictions = self.model.predict_proba(input_scaled)
        return {
            "heart_disease_risk": predictions[0][0][1],
            "stroke_risk": predictions[1][0][1]
        }

# Global model instance
disease_model = DiseaseRiskModel()

def predict_diseases(user_input):
    return disease_model.predict(user_input)

# # For testing directly
# if __name__ == "__main__":
#     test_input = {
#         "age": 58,
#         "sex": 1,
#         "bmi": 29.1,
#         "weight": 82,
#         "blood_pressure": 138,
#         "heart_rate": 75,
#         "smoking_status": 1,
#         "cholesterol": 220,
#         "glucose": 102
#     }
#     result = predict_diseases(test_input)
#     print("Prediction Results:")
#     for key, val in result.items():
#         print(f"{key.replace('_', ' ').title()}: {val:.2f}")
