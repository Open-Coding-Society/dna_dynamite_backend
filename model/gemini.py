# from flask import g
# from __init__ import app, db
# from datetime import datetime
# from sqlalchemy import Integer, String, Text, JSON, Boolean


# class TriviaResponse(db.Model):
#     __tablename__ = 'trivia_responses'  # Explicitly set the table name
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)  # Changed to Integer
#     question = db.Column(db.Text, nullable=False)
#     answer_options = db.Column(db.JSON, nullable=False)
#     selected_answer = db.Column(db.String(1), nullable=False)
#     correct_answer = db.Column(db.String(1), nullable=False)
#     explanation = db.Column(db.Text, nullable=False)
#     is_correct = db.Column(db.Boolean, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
#     user = db.relationship('User', backref='trivia_responses')  # Relationship with User



