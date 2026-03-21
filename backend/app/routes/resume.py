from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.agents.resume_agent import ResumeAgent


resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/generate-ats', methods=['POST'])
@jwt_required()
def generate_ats_resume():
    data = request.get_json(silent=True) or {}

    resume_text = (data.get('resume_text') or '').strip()
    job_description = (data.get('job_description') or '').strip()

    if not resume_text:
        return jsonify({'error': 'resume_text is required'}), 400

    if not job_description:
        return jsonify({'error': 'job_description is required'}), 400

    try:
        agent = ResumeAgent()
        result = agent.generate_ats_resume(resume_text, job_description)

        if result.get('success'):
            return jsonify(
                {
                    'success': True,
                    'optimized_resume': result.get('optimized_resume'),
                    'extracted_keywords': result.get('extracted_keywords'),
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
                'error': f'Failed to generate ATS resume: {str(e)}',
            }
        ), 500
