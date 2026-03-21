from typing import Any, Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.agents.base_agent import BaseAgent


class ResumeAgent(BaseAgent):
    def generate_ats_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        try:
            if not resume_text or not resume_text.strip():
                return {'success': False, 'error': 'resume_text is required.'}

            if not job_description or not job_description.strip():
                return {'success': False, 'error': 'job_description is required.'}

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        'You are an expert ATS resume writer. Optimize resumes for ATS relevance while keeping all claims truthful.',
                    ),
                    (
                        'human',
                        """Rewrite the following resume to better match the target job description.

Requirements:
1. Do not invent qualifications, roles, or achievements.
2. Improve ATS readability with clean section structure and concise bullet points.
3. Align wording with the role's key requirements and skills.
4. Keep the output professional and ready to submit.

Target Job Description:
{job_description}

Original Resume:
{resume_text}

Return only the rewritten ATS-optimized resume text.""",
                    ),
                ]
            )

            chain = prompt | self.llm | StrOutputParser()
            optimized_resume = chain.invoke(
                {
                    'resume_text': resume_text.strip(),
                    'job_description': job_description.strip(),
                }
            ).strip()

            return {'success': True, 'optimized_resume': optimized_resume}
        except Exception as error:
            return self.handle_error(error, context='Failed to generate ATS resume')
