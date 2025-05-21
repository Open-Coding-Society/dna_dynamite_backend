from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
#from model.post import Post
from __init__ import app, db
from api.jwt_authorize import token_required
from sqlalchemy.exc import IntegrityError
from model.user import User

    
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
def get_or_create_user(uid):
    user = User.query.filter_by(_uid=uid).first()
    if not user:
        user = User(uid, uid, 'password')  # Fill with whatever is valid for your User model
        db.session.add(user)
        db.session.commit()
    return user

def initScores(): 
    """
The initUsers function creates the User table and adds tester data to the table.

Uses:
    The db ORM methods to create the table.

Instantiates:
    User objects with tester data.

Raises:
    IntegrityError: An error occurred when adding the tester data to the table.
"""
with app.app_context():
        db.create_all()

        # Get or create test users
        risha = get_or_create_user('risha')
        hannah = get_or_create_user('hannah')
        shriya = get_or_create_user('shriya')

        # Add high scores
        scores = [
            HighScore(user_id=risha.id, score=0),
            HighScore(user_id=hannah.id, score=0),
            HighScore(user_id=shriya.id, score=1)
        ]

        for score in scores:
            try:
                score.create()
            except IntegrityError:
                db.session.rollback()








