from datetime import datetime

from app import db


class Job(db.Model):
	__tablename__ = 'jobs'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
	title = db.Column(db.String(255), nullable=False)
	company = db.Column(db.String(255), nullable=False)
	link = db.Column(db.String(1000), nullable=True)
	description = db.Column(db.Text, nullable=True)
	location = db.Column(db.String(255), nullable=True)
	salary = db.Column(db.String(120), nullable=True)
	source = db.Column(db.String(120), nullable=True)
	added_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
