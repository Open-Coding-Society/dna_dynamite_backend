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
        data = request.get_json(force=True)

        # Required input fields for prediction
        required_fields = [
            "age", "sex", "bmi", "weight", "blood_pressure",
            "heart_rate", "smoking_status", "cholesterol", "glucose"
        ]

        # Check for missing fields
        missing = [field for field in required_fields if field not in data]
        if missing:
            return jsonify({"error": f"Missing field(s): {', '.join(missing)}"}), 400

        # Run prediction, ouput test 
        prediction = predict_diseases(data)

        return jsonify({
            "message": "Prediction successful",
            "data": {
                "heart_disease_10yr_risk": round(prediction["heart_disease_10yr_risk"], 4), # changed backend variable name, modify on frontend too
                "stroke_10yr_risk": round(prediction["stroke_10yr_risk"], 4)
            }
        })

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500
