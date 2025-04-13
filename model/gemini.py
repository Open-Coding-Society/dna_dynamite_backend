from __init__ import db

class TriviaQuestion(db.Model):
    __tablename__ = 'trivia_questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer_options = db.Column(db.JSON, nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text, nullable=False)

    def __init__(self, question, answer_options, correct_answer, explanation):
        self.question = question
        self.answer_options = answer_options
        self.correct_answer = correct_answer
        self.explanation = explanation

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer_options": self.answer_options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation
        }

# ✅ Move this outside the class
class TriviaResponse(db.Model):
    __tablename__ = 'trivia_responses'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('trivia_questions.id'), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def __init__(self, question_id, selected_answer, is_correct):
        self.question_id = question_id
        self.selected_answer = selected_answer
        self.is_correct = is_correct

    def to_dict(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "selected_answer": self.selected_answer,
            "is_correct": self.is_correct
        }
