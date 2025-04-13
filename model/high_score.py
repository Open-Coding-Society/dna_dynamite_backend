from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
#from model.post import Post
from __init__ import db
from api.jwt_authorize import token_required
    
class HighScore(db.Model):
    __tablename__ = 'high_scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)
    channel_id = db.Column(db.Integer, default=7)  # ✅ link to High Scores channel

    def __init__(self, user_id, score=0, channel_id=7):
        self.user_id = user_id
        self.score = score
        self.channel_id = channel_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read(self):
        return {
            "user_id": self.user_id,
            "score": self.score,
            "channel_id": self.channel_id,
        }

