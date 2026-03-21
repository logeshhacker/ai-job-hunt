from datetime import datetime

from app import db


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False, default='applied')
    resume_used = db.Column(db.Text, nullable=True)
    cover_letter_used = db.Column(db.Text, nullable=True)
    applied_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    interview_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
