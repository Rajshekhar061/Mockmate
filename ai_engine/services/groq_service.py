"""
Groq AI Service for interacting with Groq API.
Handles resume analysis and interview question generation.
"""

import json
import logging
import os
from typing import Dict, Optional, Any
from groq import Groq

from ai_engine.prompts.resume_prompt import get_resume_analysis_prompt
from ai_engine.prompts.interview_prompt import get_interview_questions_prompt
from ai_engine.prompts.feedback_prompt import get_interview_feedback_prompt
from ai_engine.prompts.analytics_prompt import get_analytics_recommendation_prompt

logger = logging.getLogger(__name__)


class GroqService:
    """
    Service class for interacting with Groq API.
    Provides methods for AI-powered resume analysis and interview preparation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq service.
        
        Args:
            api_key (Optional[str]): Groq API key. If not provided, reads from environment.
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables or parameters")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.timeout = 30

    def analyze_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a resume using Groq API.
        
        Args:
            resume_text (str): The extracted text from the resume
            job_description (Optional[str]): Target job description for better matching
            
        Returns:
            Dict[str, Any]: Analysis results containing ATS score, strengths, weaknesses, etc.
        """
        try:
            prompt = get_resume_analysis_prompt(resume_text, job_description)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ATS (Applicant Tracking System) specialist and career counselor. Analyze the provided resume and return ONLY valid JSON output with no additional text or markdown."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                timeout=self.timeout,
            )
            
            # Extract the response content
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON response
            analysis_result = json.loads(response_text)
            
            logger.info(f"Successfully analyzed resume. ATS Score: {analysis_result.get('ats_score')}")
            
            return analysis_result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response as JSON: {str(e)}")
            return {
                'error': 'Failed to parse AI response',
                'details': str(e),
                'ats_score': 0,
                'strengths': [],
                'weaknesses': [],
                'suggestions': []
            }
        except Exception as e:
            logger.error(f"Error analyzing resume with Groq: {str(e)}")
            return {
                'error': 'Failed to analyze resume',
                'details': str(e),
                'ats_score': 0,
                'strengths': [],
                'weaknesses': [],
                'suggestions': []
            }

    def generate_interview_questions(
    self,
    resume_text: str = "",
    role: str = "Software Engineer",
    difficulty: str = "medium",
    interview_type: str = "technical",
    count: int = 5
) -> Dict[str, Any]:
        """
        Generate mock interview questions based on resume.
        
        Args:
            resume_text (str): The extracted resume text
            role (str): The target job role
            
        Returns:
            Dict[str, Any]: Generated interview questions and topics
        """
        try:
            prompt = f"""
Based on this resume, generate {count} targeted {interview_type} interview questions

Difficulty Level: {difficulty}

Resume:
{resume_text[:2000]}

Return ONLY a valid JSON object...
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional interviewer. Generate relevant interview questions. Return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=1500,
                timeout=self.timeout,
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean markdown if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            response_text = response_text.strip()
            result = json.loads(response_text)
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating interview questions: {str(e)}")
            return {
                'error': 'Failed to generate questions',
                'questions': [],
                'focus_areas': []
            }

    def evaluate_interview_answer(
        self,
        question: str,
        user_answer: str,
        role: str = 'Software Engineer',
        difficulty: str = 'medium',
        interview_type: str = 'technical',
    ) -> Dict[str, Any]:
        """Evaluate a user's interview answer using Groq AI."""
        try:
            prompt = get_interview_feedback_prompt(
                question=question,
                user_answer=user_answer,
                role=role,
                difficulty=difficulty,
                interview_type=interview_type,
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a skilled interviewer and recruiter. Provide a concise evaluation of the candidate response and return ONLY valid JSON.'
                    },
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
                temperature=0.7,
                max_tokens=1200,
                timeout=self.timeout,
            )

            response_text = response.choices[0].message.content.strip()
            if response_text.startswith('```'):
                content_parts = response_text.split('```')
                if len(content_parts) >= 2:
                    response_text = content_parts[1]
            response_text = response_text.strip()
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse interview evaluation JSON: {str(e)}")
            return {
                'error': 'Failed to parse evaluation response',
                'score': 0,
                'feedback_summary': 'Unable to parse AI feedback.',
                'strengths': [],
                'weaknesses': [],
                'ideal_answer': '',
                'suggestions': [],
            }
        except Exception as e:
            logger.error(f"Error evaluating interview answer: {str(e)}")
            return {
                'error': 'Failed to evaluate answer',
                'score': 0,
                'feedback_summary': 'AI evaluation is unavailable.',
                'strengths': [],
                'weaknesses': [],
                'ideal_answer': '',
                'suggestions': [],
            }

    def generate_analytics_recommendations(self, summary: str) -> dict:
        """Generate analytics-based improvement recommendations."""
        try:
            prompt = get_analytics_recommendation_prompt(summary)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are an expert career coach and interview analyst. Provide targeted improvement recommendations based on the summary provided and return only valid JSON.'
                    },
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
                temperature=0.7,
                max_tokens=1200,
                timeout=self.timeout,
            )

            response_text = response.choices[0].message.content.strip()
            if response_text.startswith('```'):
                parts = response_text.split('```')
                if len(parts) >= 2:
                    response_text = parts[1]
            response_text = response_text.strip()
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse analytics recommendation JSON: {str(e)}")
            return {
                'error': 'Failed to parse analytics recommendation response',
                'recommended_topics': [],
                'practice_suggestions': [],
                'improvement_roadmap': []
            }
        except Exception as e:
            logger.error(f"Error generating analytics recommendations: {str(e)}")
            return {
                'error': 'Failed to generate analytics recommendations',
                'recommended_topics': [],
                'practice_suggestions': [],
                'improvement_roadmap': []
            }

    def generate_response(self, prompt: str, system_message: str = "You are a helpful assistant.", max_tokens: int = 1000) -> Optional[str]:
        """
        Generic method to generate a response from Groq.
        
        Args:
            prompt (str): User prompt
            system_message (str): System message for context
            max_tokens (int): Maximum tokens in response
            
        Returns:
            Optional[str]: Generated response or None if failed
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=max_tokens,
                timeout=self.timeout,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return None

    def health_check(self) -> bool:
        """
        Test connection to Groq API.
        
        Returns:
            bool: True if API is accessible, False otherwise
        """
        try:
            response = self.generate_response(
                "Say 'OK' if you can read this.",
                "You are a helpful assistant.",
                max_tokens=10
            )
            return response is not None
        except Exception as e:
            logger.error(f"Groq API health check failed: {str(e)}")
            return False
