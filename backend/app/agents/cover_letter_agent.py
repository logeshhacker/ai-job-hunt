from typing import Any, Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.agents.base_agent import BaseAgent


class CoverLetterAgent(BaseAgent):
    def generate_cover_letter(
        self, resume_text: str, job_description: str, company_name: str
    ) -> Dict[str, Any]:
        try:
            if not resume_text or not resume_text.strip():
                return {
                    'success': False,
                    'error': 'resume_text is required.',
                }

            if not job_description or not job_description.strip():
                return {
                    'success': False,
                    'error': 'job_description is required.',
                }

            if not company_name or not company_name.strip():
                return {
                    'success': False,
                    'error': 'company_name is required.',
                }

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        'system',
                        'You are an expert cover letter writer who creates concise, personalized, professional letters based only on provided facts.',
                    ),
                    (
                        'human',
                        """Generate a professional, personalized cover letter based on the provided resume, job description, and company information.

Guidelines:
1. Write a compelling opening that shows genuine interest in the company and role.
2. Highlight key achievements and skills from the resume that align with the job requirements.
3. Demonstrate knowledge of the company and how your background fits their needs.
4. Keep the tone professional, confident, and genuine.
5. Structure as a proper cover letter with opening, body paragraphs, and closing.
6. Keep the letter concise (usually 3-4 paragraphs, under 400 words).
7. Do not invent or exaggerate qualifications.

Candidate Resume:
{resume_text}

Target Job Description:
{job_description}

Company Name:
{company_name}

Generate a professional cover letter:""",
                    ),
                ]
            )

            chain = prompt | self.llm | StrOutputParser()
            cover_letter = chain.invoke(
                {
                    'resume_text': resume_text,
                    'job_description': job_description,
                    'company_name': company_name,
                }
            ).strip()

            return {
                'success': True,
                'cover_letter': cover_letter,
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to generate cover letter')
