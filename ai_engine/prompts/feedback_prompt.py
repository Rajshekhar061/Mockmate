"""Interview feedback prompts for Groq AI."""


def get_interview_feedback_prompt(
    question: str,
    user_answer: str,
    role: str,
    difficulty: str,
    interview_type: str,
) -> str:
    """Generate the prompt for evaluating an interview answer."""
    return f"""You are a knowledgeable hiring manager evaluating interview answers.

QUESTION:
{question}

CANDIDATE ANSWER:
{user_answer}

ROLE:
{role}

DIFFICULTY:
{difficulty}

INTERVIEW TYPE:
{interview_type}

Evaluate the response and return ONLY valid JSON with no extra text.

RESPONSE FORMAT:
{{
  "score": <integer 0-100>,
  "feedback_summary": "<brief evaluation>",
  "strengths": ["<strength1>", "<strength2>"],
  "weaknesses": ["<weakness1>", "<weakness2>"],
  "ideal_answer": "<ideal answer text>",
  "suggestions": ["<suggestion1>", "<suggestion2>"]
}}

Important rules:
- Return only valid JSON.
- No markdown or code fences.
- Keep the evaluation concise and directly tied to the answer.
"""
