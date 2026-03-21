import re
from collections import Counter
from importlib import import_module
from typing import Any, Dict, List

try:
    LLMChain = import_module('langchain.chains').LLMChain
except ModuleNotFoundError:
    LLMChain = import_module('langchain_community.chains').LLMChain

PromptTemplate = import_module('langchain_core.prompts').PromptTemplate

from app.agents.base_agent import BaseAgent


class ResumeAgent(BaseAgent):
    def _extract_keywords(self, job_description: str, max_keywords: int = 20) -> List[str]:
        # Keep common stop words out so technical/domain terms dominate.
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'have', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'you', 'your', 'our', 'we',
            'this', 'those', 'these', 'their', 'they', 'them', 'who', 'what',
            'when', 'where', 'why', 'how', 'job', 'role', 'position', 'team',
            'candidate', 'required', 'preferred', 'experience', 'skills',
        }

        words = re.findall(r"[A-Za-z][A-Za-z0-9+.#-]{1,}", job_description.lower())
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]

        keyword_counts = Counter(filtered_words)
        return [keyword for keyword, _ in keyword_counts.most_common(max_keywords)]

    def generate_ats_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
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

            extracted_keywords = self._extract_keywords(job_description)
            keyword_string = ', '.join(extracted_keywords)

            prompt = PromptTemplate(
                input_variables=['resume_text', 'job_description', 'keywords'],
                template="""You are an expert ATS resume writer. Rewrite the resume to better align with the target job description while preserving truthful experience and facts.

Rules:
1. Keep the content honest and do not invent experience.
2. Improve keyword alignment for ATS parsing.
3. Use concise, impact-focused bullet points with measurable outcomes when possible.
4. Prioritize the most relevant skills and achievements for this role.

Target Job Description:
{job_description}

Important Keywords To Incorporate Naturally:
{keywords}

Original Resume:
{resume_text}

Return only the ATS-optimized resume text.""",
            )

            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = chain.invoke(
                {
                    'resume_text': resume_text,
                    'job_description': job_description,
                    'keywords': keyword_string,
                }
            )

            optimized_resume = result.get('text', '').strip() if isinstance(result, dict) else str(result).strip()

            return {
                'success': True,
                'optimized_resume': optimized_resume,
                'extracted_keywords': extracted_keywords,
            }
        except Exception as error:
            return self.handle_error(error, context='Failed to generate ATS resume')
