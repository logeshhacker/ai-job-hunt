from importlib import import_module
from typing import Any, Dict, List, Optional

try:
    LLMChain = import_module('langchain.chains').LLMChain
except ModuleNotFoundError:
    LLMChain = import_module('langchain_community.chains').LLMChain

ConversationBufferMemory = import_module('langchain.memory').ConversationBufferMemory
PromptTemplate = import_module('langchain_core.prompts').PromptTemplate

from app.agents.base_agent import BaseAgent


class ChatAgent(BaseAgent):
    def __init__(self, temperature: float = 0.7, model_name: str = 'gpt-3.5-turbo'):
        super().__init__(temperature=temperature, model_name=model_name)

        self.memory = ConversationBufferMemory(
            memory_key='chat_history',
            input_key='input',
        )

        self.prompt = PromptTemplate(
            input_variables=['chat_history', 'input'],
            template="""You are an expert career coach and job hunting advisor. Provide helpful, practical advice to job seekers.

Your areas of expertise include:
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
        )

        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            verbose=False,
        )

    def get_response(
        self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        try:
            if not message or not message.strip():
                return {
                    'success': False,
                    'error': 'Message cannot be empty.',
                }

            # If conversation_history is provided, reconstruct memory state
            if conversation_history:
                self.memory.clear()
                for exchange in conversation_history:
                    if 'user' in exchange and 'assistant' in exchange:
                        self.memory.save_context(
                            {'input': exchange['user']},
                            {'output': exchange['assistant']},
                        )

            response = self.chain.invoke({'input': message.strip()})

            assistant_message = response.get('text', '').strip() if isinstance(response, dict) else str(response).strip()

            return {
                'success': True,
                'response': assistant_message,
                'message': message.strip(),
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to generate chat response')

    def clear_memory(self) -> Dict[str, Any]:
        try:
            self.memory.clear()
            return {
                'success': True,
                'message': 'Chat history cleared.',
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to clear chat history')

    def get_memory_summary(self) -> Dict[str, Any]:
        try:
            memory_content = self.memory.buffer if hasattr(self.memory, 'buffer') else ''
            return {
                'success': True,
                'memory_content': memory_content,
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to retrieve chat history')
