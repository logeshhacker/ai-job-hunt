from typing import Any, Dict, List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.agents.base_agent import BaseAgent


class ChatAgent(BaseAgent):
    def __init__(self, temperature: float = 0.7, model_name: str = 'gpt-3.5-turbo'):
        super().__init__(temperature=temperature, model_name=model_name)
        self.conversation_history: List[Dict[str, str]] = []

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    'You are an expert career coach and job hunting advisor. Provide practical, actionable support.',
                ),
                (
                    'human',
                    """Your areas of expertise include:
- Resume optimization and tailoring
- Cover letter strategies
- Interview preparation
- Job search techniques
- Career development
- Salary negotiations
- LinkedIn profile optimization
- Portfolio building
- Skill development for career growth
- Navigating job market trends

Always:
1. Provide actionable, specific advice.
2. Ask clarifying questions when needed.
3. Be encouraging and supportive.
4. Reference best practices in job hunting.
5. Personalize advice based on the conversation context.

Chat History:
{chat_history}

User: {input}

Career Advisor:""",
                ),
            ]
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    def _build_chat_history(self, history: List[Dict[str, str]]) -> str:
        lines = []
        for exchange in history:
            user_text = (exchange.get('user') or '').strip()
            assistant_text = (exchange.get('assistant') or '').strip()
            if user_text:
                lines.append(f'User: {user_text}')
            if assistant_text:
                lines.append(f'Career Advisor: {assistant_text}')
        return '\n'.join(lines)

    def get_response(
        self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        try:
            if not message or not message.strip():
                return {
                    'success': False,
                    'error': 'Message cannot be empty.',
                }

            if conversation_history is not None:
                self.conversation_history = conversation_history

            chat_history = self._build_chat_history(self.conversation_history)

            assistant_message = self.chain.invoke(
                {'chat_history': chat_history, 'input': message.strip()}
            ).strip()

            self.conversation_history.append(
                {'user': message.strip(), 'assistant': assistant_message}
            )

            return {
                'success': True,
                'response': assistant_message,
                'message': message.strip(),
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to generate chat response')

    def clear_memory(self) -> Dict[str, Any]:
        try:
            self.conversation_history = []
            return {
                'success': True,
                'message': 'Chat history cleared.',
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to clear chat history')

    def get_memory_summary(self) -> Dict[str, Any]:
        try:
            memory_content = self._build_chat_history(self.conversation_history)
            return {
                'success': True,
                'memory_content': memory_content,
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to retrieve chat history')
