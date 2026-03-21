import os
from typing import Any, Dict, Optional

from langchain_openai import ChatOpenAI


class BaseAgent:
	def __init__(self, temperature: float = 0.7, model_name: str = 'gpt-3.5-turbo'):
		self.temperature = temperature
		self.model_name = model_name
		self.api_key = os.getenv('OPENAI_API_KEY')

		if not self.api_key:
			raise ValueError('OPENAI_API_KEY environment variable is not set.')

		self.llm = ChatOpenAI(
			model=self.model_name,
			temperature=self.temperature,
			api_key=self.api_key,
		)

	def handle_error(self, error: Exception, context: Optional[str] = None) -> Dict[str, Any]:
		message = str(error)
		if context:
			message = f'{context}: {message}'

		return {
			'success': False,
			'error': message,
			'error_type': error.__class__.__name__,
		}
