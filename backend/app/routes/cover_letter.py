from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.agents.cover_letter_agent import CoverLetterAgent


cover_letter_bp = Blueprint('cover_letter', __name__)


@cover_letter_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_cover_letter():
    data = request.get_json(silent=True) or {}

    resume_text = (data.get('resume_text') or '').strip()
    job_description = (data.get('job_description') or '').strip()
    company_name = (data.get('company_name') or '').strip()

    if not resume_text:
        return jsonify({'error': 'resume_text is required'}), 400

    if not job_description:
        return jsonify({'error': 'job_description is required'}), 400

    if not company_name:
        return jsonify({'error': 'company_name is required'}), 400

    try:
        agent = CoverLetterAgent()
        result = agent.generate_cover_letter(resume_text, job_description, company_name)

        if result.get('success'):
            return jsonify(
                {
                    'success': True,
                    'cover_letter': result.get('cover_letter'),
                }
            ), 200
        else:
            return jsonify(
                {
                    'success': False,
                    'error': result.get('error'),
                }
            ), 400
    except Exception as e:
        return jsonify(
            {
                'success': False,
                'error': f'Failed to generate cover letter: {str(e)}',
            }
        ), 500
