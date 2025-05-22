from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from model.high_score import HighScore
from api.jwt_authorize import token_required

score_api = Blueprint('score_api', __name__, url_prefix='/api')
api = Api(score_api)

class ScoreAPI:
    class _UserScore(Resource):
        @token_required()
        def get(self):
            current_user = g.current_user
            score = HighScore.query.filter_by(user_id=current_user.id).first()
            if not score:
                return jsonify({"score": 0})
            return jsonify(score.read())
        

    class _AllUsersScore(Resource):
        def get(self):
            scores = HighScore.query.all()
            if not scores:
                return jsonify([])

            all_scores = [score.read() for score in scores]
            return jsonify(all_scores)


    class _UpdateScore(Resource):
        @token_required()
        def put(self):
            current_user = g.current_user
            data = request.get_json()
            new_score = data.get("score")

            if new_score is None:
                return {"message": "Score is required"}, 400

            # ✅ Check if this user already has a high score
            high_score = HighScore.query.filter_by(user_id=current_user.id).first()
            high_score_updated = False  # New flag

            if high_score:
                if new_score > high_score.score:
                    high_score.score = new_score
                    high_score.update()
                    high_score_updated = True
                    
            else:
                # ✅ Create a new record if none exists
                high_score = HighScore(user_id=current_user.id, score=new_score, channel_id=7)
                high_score.create()
                high_score_updated = True 

            return jsonify({
                **high_score.read(),
                "high_score_updated": high_score_updated  # 👈 Add this to response
            })


    class _DeleteScore(Resource):
        @token_required()
        def delete(self):
            data = request.get_json()
            user_id = data.get("user_id")
            if not user_id:
                return {"message": "User ID required"}, 400

            score = HighScore.query.filter_by(user_id=user_id).first()
            if not score:
                return {"message": "Score not found"}, 404

            score.delete()
            return {"message": "Score deleted"}, 200

api.add_resource(ScoreAPI._UserScore, '/score/user')
api.add_resource(ScoreAPI._AllUsersScore, '/score/all_users')
api.add_resource(ScoreAPI._UpdateScore, '/score')
api.add_resource(ScoreAPI._DeleteScore, '/score/admin/delete')
