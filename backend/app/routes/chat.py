from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.agents.chat_agent import ChatAgent


chat_bp = Blueprint('chat', __name__)

# Store a single ChatAgent instance for conversation continuity
_chat_agent = None


def get_chat_agent():
    global _chat_agent
    if _chat_agent is None:
        _chat_agent = ChatAgent()
    return _chat_agent


@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json(silent=True) or {}

    message = (data.get('message') or '').strip()

    if not message:
        return jsonify({'error': 'message is required'}), 400

    try:
        agent = get_chat_agent()
        conversation_history = data.get('conversation_history', None)
        result = agent.get_response(message, conversation_history=conversation_history)

        if result.get('success'):
            return jsonify(
                {
                    'success': True,
                    'response': result.get('response'),
                    'message': result.get('message'),
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
                'error': f'Failed to get chat response: {str(e)}',
            }
        ), 500


@chat_bp.route('/clear', methods=['POST'])
@jwt_required()
def clear_history():
    try:
        agent = get_chat_agent()
        result = agent.clear_memory()

        if result.get('success'):
            return jsonify(
                {
                    'success': True,
                    'message': 'Chat history cleared.',
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
                'error': f'Failed to clear chat history: {str(e)}',
            }
        ), 500
