from datetime import date, datetime, timedelta
from io import BytesIO

from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from openpyxl import Workbook
from sqlalchemy import func

from app.models.application import Application
from app.models.job import Job


analytics_bp = Blueprint('analytics', __name__)


def _get_current_user_id():
	identity = get_jwt_identity()
	try:
		return int(identity)
	except (TypeError, ValueError):
		return None


@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
def summary():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	total_jobs = Job.query.filter_by(user_id=user_id).count()
	applications = Application.query.filter_by(user_id=user_id).all()

	applied_count = sum(1 for app in applications if (app.status or '').lower() == 'applied')
	interviews_count = sum(1 for app in applications if (app.status or '').lower() == 'interview')
	offers_count = sum(1 for app in applications if (app.status or '').lower() == 'offer')
	rejected_count = sum(1 for app in applications if (app.status or '').lower() == 'rejected')

	total_applications = len(applications)
	success_rate = round((offers_count / total_applications) * 100, 2) if total_applications else 0.0

	return jsonify(
		{
			'success': True,
			'total_jobs': total_jobs,
			'applied': applied_count,
			'interviews': interviews_count,
			'offers': offers_count,
			'rejected': rejected_count,
			'success_rate': success_rate,
		}
	), 200


@analytics_bp.route('/daily', methods=['GET'])
@jwt_required()
def daily_counts():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	today = datetime.utcnow().date()
	start_date = today - timedelta(days=29)

	rows = (
		Application.query.with_entities(
			func.date(Application.applied_date).label('applied_day'),
			func.count(Application.id).label('count'),
		)
		.filter(Application.user_id == user_id)
		.filter(Application.applied_date >= datetime.combine(start_date, datetime.min.time()))
		.group_by(func.date(Application.applied_date))
		.all()
	)

	counts_by_day = {str(row.applied_day): row.count for row in rows}

	daily_data = []
	for index in range(30):
		day = start_date + timedelta(days=index)
		day_key = day.isoformat()
		daily_data.append(
			{
				'date': day_key,
				'count': counts_by_day.get(day_key, 0),
			}
		)

	return jsonify({'success': True, 'daily_applications': daily_data}), 200


@analytics_bp.route('/export-excel', methods=['GET'])
@jwt_required()
def export_excel():
	user_id = _get_current_user_id()
	if user_id is None:
		return jsonify({'success': False, 'error': 'Invalid user identity in token'}), 401

	applications = (
		Application.query.with_entities(
			Job.title,
			Job.company,
			Application.status,
			Application.applied_date,
		)
		.join(Job, Application.job_id == Job.id)
		.filter(Application.user_id == user_id)
		.filter(Job.user_id == user_id)
		.order_by(Application.applied_date.desc())
		.all()
	)

	workbook = Workbook()
	sheet = workbook.active
	sheet.title = 'Applications'
	sheet.append(['Job Title', 'Company', 'Status', 'Applied Date'])

	for title, company, status, applied_date in applications:
		sheet.append(
			[
				title,
				company,
				status,
				applied_date.strftime('%Y-%m-%d %H:%M:%S') if applied_date else '',
			]
		)

	output = BytesIO()
	workbook.save(output)
	output.seek(0)

	filename = f'applications_{date.today().isoformat()}.xlsx'
	return send_file(
		output,
		as_attachment=True,
		download_name=filename,
		mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
	)
