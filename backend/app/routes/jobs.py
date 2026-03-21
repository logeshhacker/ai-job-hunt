from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models.application import Application
from app.models.job import Job


jobs_bp = Blueprint('jobs', __name__)


def _get_current_user_id():
	identity = get_jwt_identity()
	try:
		return int(identity)
	except (TypeError, ValueError):
		return None


def _parse_int(value):
	try:
		return int(value)
	except (TypeError, ValueError):
		return None


@jobs_bp.route('/add', methods=['POST'])
@jwt_required()
def add_job():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	data = request.get_json(silent=True) or {}

	title = (data.get('title') or '').strip()
	company = (data.get('company') or '').strip()

	if not title:
		return jsonify({'success': False, 'error': 'title is required'}), 400
	if not company:
		return jsonify({'success': False, 'error': 'company is required'}), 400

	job = Job(
		user_id=user_id,
		title=title,
		company=company,
		link=(data.get('link') or '').strip() or None,
		description=(data.get('description') or '').strip() or None,
		location=(data.get('location') or '').strip() or None,
		salary=(data.get('salary') or '').strip() or None,
		source=(data.get('source') or '').strip() or None,
	)

	db.session.add(job)
	db.session.commit()

	return jsonify({'success': True, 'job_id': job.id}), 201


@jobs_bp.route('/list', methods=['GET'])
@jwt_required()
def list_jobs():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	jobs = Job.query.filter_by(user_id=user_id).order_by(Job.added_date.desc()).all()

	return jsonify(
		{
			'success': True,
			'jobs': [
				{
					'id': job.id,
					'title': job.title,
					'company': job.company,
					'link': job.link,
					'description': job.description,
					'location': job.location,
					'salary': job.salary,
					'source': job.source,
					'added_date': job.added_date.isoformat() if job.added_date else None,
				}
				for job in jobs
			],
		}
	), 200


@jobs_bp.route('/mark-applied', methods=['POST'])
@jwt_required()
def mark_applied():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	data = request.get_json(silent=True) or {}
	job_id = _parse_int(data.get('job_id'))
	resume_id = data.get('resume_id')
	cover_letter_id = data.get('cover_letter_id')

	if not job_id:
		return jsonify({'success': False, 'error': 'job_id is required'}), 400

	job = Job.query.filter_by(id=job_id, user_id=user_id).first()
	if not job:
		return jsonify({'success': False, 'error': 'Job not found'}), 404

	application = Application.query.filter_by(user_id=user_id, job_id=job.id).first()
	if not application:
		application = Application(user_id=user_id, job_id=job.id)
		db.session.add(application)

	application.status = 'applied'
	application.resume_used = str(resume_id) if resume_id is not None else None
	application.cover_letter_used = str(cover_letter_id) if cover_letter_id is not None else None

	db.session.commit()

	return jsonify({'success': True, 'application_id': application.id}), 200


@jobs_bp.route('/update-status', methods=['PUT'])
@jwt_required()
def update_application_status():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	data = request.get_json(silent=True) or {}
	application_id = _parse_int(data.get('application_id'))
	job_id = _parse_int(data.get('job_id'))
	status = (data.get('status') or '').strip()
	interview_date = data.get('interview_date')
	notes = data.get('notes')

	if not status:
		return jsonify({'success': False, 'error': 'status is required'}), 400

	application = None
	if application_id is not None:
		application = Application.query.filter_by(id=application_id, user_id=user_id).first()
	elif job_id is not None:
		application = Application.query.filter_by(job_id=job_id, user_id=user_id).first()
	else:
		return jsonify({'success': False, 'error': 'application_id or job_id is required'}), 400

	if not application:
		return jsonify({'success': False, 'error': 'Application not found'}), 404

	application.status = status
	if interview_date is not None:
		if interview_date == '':
			application.interview_date = None
		else:
			try:
				application.interview_date = datetime.fromisoformat(str(interview_date))
			except ValueError:
				return jsonify({'success': False, 'error': 'interview_date must be ISO format'}), 400
	if notes is not None:
		application.notes = str(notes)

	db.session.commit()

	return jsonify({'success': True, 'application_id': application.id, 'status': application.status}), 200


@jobs_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_job():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	data = request.get_json(silent=True) or {}
	job_id = _parse_int(data.get('job_id') or request.args.get('job_id'))
	if not job_id:
		return jsonify({'success': False, 'error': 'job_id is required'}), 400

	job = Job.query.filter_by(id=job_id, user_id=user_id).first()
	if not job:
		return jsonify({'success': False, 'error': 'Job not found'}), 404

	Application.query.filter_by(user_id=user_id, job_id=job.id).delete()
	db.session.delete(job)
	db.session.commit()

	return jsonify({'success': True, 'message': 'Job deleted'}), 200
