from flask import Blueprint, request, jsonify
from flask_restful import Api
from __init__ import app
from model.predict_disease import predict_diseases

# Create blueprint
predict_api = Blueprint('predict_api', __name__, url_prefix='/api')
api = Api(predict_api)

@predict_api.route("/predict_disease", methods=["POST"])
def predict_disease():
    """API endpoint to predict heart disease and stroke risk from user input"""
    try:
        data = request.get_json()

        # Validate required keys based on the model
        required_fields = [
            "age", "sex", "bmi", "weight", "blood_pressure",
            "heart_rate", "smoking_status", "cholesterol", "glucose"
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Get prediction from model
        prediction = predict_diseases(data)

        return jsonify({
            "message": "Prediction successful",
            "data": prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
