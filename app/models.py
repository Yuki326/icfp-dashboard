import db

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    user_input = db.Column(db.Text, nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    submission_time = db.Column(db.DateTime, server_default=db.func.now())

    

