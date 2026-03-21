"""WSGI entry point for the Flask backend."""

import os
import traceback

from app import create_app


try:
	app = create_app(config_name=os.getenv('FLASK_ENV', 'development'))
	print('[startup] Flask app created successfully.')
except Exception as exc:
	print(f'[startup] Failed to create Flask app: {exc}')
	traceback.print_exc()
	raise


if __name__ == '__main__':
	debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
	print(f'[startup] Starting Flask server on http://127.0.0.1:5000 (debug={debug_mode})')

	try:
		app.run(debug=debug_mode)
	except Exception as exc:
		print(f'[startup] Server failed to start: {exc}')
		traceback.print_exc()
		raise
