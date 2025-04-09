from __init__ import db

class TriviaQuestion(db.Model):
    """
    TriviaQuestion Model
    Represents a trivia question about DNA/genetics.
    """
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
