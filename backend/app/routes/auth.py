from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app import db, jwt
from app.models.user import User


auth_bp = Blueprint('auth', __name__)


def _parse_auth_payload():
	data = request.get_json(silent=True) or {}

	name = (data.get('name') or '').strip()
	email = (data.get('email') or '').strip().lower()
	password = data.get('password') or ''

	return name, email, password


@auth_bp.route('/register', methods=['POST'])
def register():
	name, email, password = _parse_auth_payload()

	if not name:
		return jsonify({'error': 'Name is required'}), 400

	if not email or '@' not in email:
		return jsonify({'error': 'Valid email is required'}), 400

	if not password or len(password) < 6:
		return jsonify({'error': 'Password must be at least 6 characters long'}), 400

	existing_user = User.query.filter_by(email=email).first()
	if existing_user:
		return jsonify({'error': 'Email is already registered'}), 409

	user = User(name=name, email=email)
	user.set_password(password)

	db.session.add(user)
	db.session.commit()

	token = create_access_token(identity=str(user.id))

	return jsonify(
		{
			'token': token,
			'user': {
				'id': user.id,
				'name': user.name,
				'email': user.email,
			},
		}
	), 201


@auth_bp.route('/login', methods=['POST'])
def login():
	_, email, password = _parse_auth_payload()

	if not email or not password:
		return jsonify({'error': 'Email and password are required'}), 400

	user = User.query.filter_by(email=email).first()
	if not user or not user.check_password(password):
		return jsonify({'error': 'Invalid email or password'}), 401

	token = create_access_token(identity=str(user.id))

	return jsonify(
		{
			'token': token,
			'user': {
				'id': user.id,
				'name': user.name,
				'email': user.email,
			},
		}
	), 200
