"""Interview generation prompts for Groq AI."""


def get_interview_questions_prompt(role: str, difficulty: str, interview_type: str, count: int = 5) -> str:
    """Generate the prompt for creating interview questions."""
    return f"""You are an expert interviewer. Generate {count} interview questions for a {difficulty} {role} position in a {interview_type} interview.

Return ONLY valid JSON with no markdown or extra text.

RESPONSE FORMAT:
{{
  "questions": [
    {{
      "question": "...",
      "topic": "...",
      "difficulty": "easy|medium|hard"
    }}
  ]
}}

Important rules:
- Return only valid JSON.
- Do not include markdown code fences.
- Ensure the JSON parses cleanly.
- Generate questions that are specific, varied, and tailored to the selected role and difficulty.
"""
