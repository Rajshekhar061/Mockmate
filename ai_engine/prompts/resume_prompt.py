"""
Resume analysis prompts for Groq AI.
Forces JSON-only responses for structured output.
"""


def get_resume_analysis_prompt(resume_text: str, job_description: str = None) -> str:
    """
    Generate the prompt for resume analysis.
    Forces JSON-only response.
    
    Args:
        resume_text (str): The extracted resume text
        job_description (str): Optional job description for context
        
    Returns:
        str: The formatted prompt
    """
    
    base_prompt = f"""Analyze the following resume and provide a comprehensive assessment. 
Return ONLY a valid JSON object with absolutely no additional text, markdown, or explanation.

RESUME:
{resume_text}
"""

    if job_description:
        base_prompt += f"""

TARGET JOB DESCRIPTION:
{job_description}

Evaluate the resume's match to this specific job description."""

    base_prompt += """

REQUIRED JSON RESPONSE FORMAT (return ONLY this JSON, no other text):
{
    "ats_score": <integer 0-100>,
    "strengths": [
        {
            "title": "<brief title>",
            "description": "<detailed explanation>",
            "impact": "high|medium|low"
        }
    ],
    "weaknesses": [
        {
            "title": "<brief title>",
            "description": "<detailed explanation>",
            "severity": "critical|high|medium|low"
        }
    ],
    "suggestions": [
        {
            "title": "<improvement title>",
            "action": "<specific action to take>",
            "priority": "high|medium|low",
            "expected_impact": "<impact on ATS score or job prospects>"
        }
    ],
    "keywords_analysis": {
        "keywords_found": ["keyword1", "keyword2"],
        "missing_keywords": ["keyword1", "keyword2"],
        "keyword_frequency": {
            "skill1": 3,
            "skill2": 2
        }
    },
    "formatting_quality": {
        "score": <0-100>,
        "issues": ["issue1", "issue2"],
        "recommendations": ["rec1", "rec2"]
    },
    "content_quality": {
        "quantification": <0-100>,
        "action_verbs": <0-100>,
        "achievement_orientation": <0-100>,
        "clarity": <0-100>
    },
    "sections_analysis": {
        "summary": {
            "present": true|false,
            "quality": "strong|good|weak|missing"
        },
        "experience": {
            "present": true|false,
            "quality": "strong|good|weak|missing",
            "suggestions": ["suggestion1", "suggestion2"]
        },
        "skills": {
            "present": true|false,
            "quality": "strong|good|weak|missing",
            "organization": "categorized|flat"
        },
        "education": {
            "present": true|false,
            "quality": "strong|good|weak|missing"
        }
    },
    "top_improvements": [
        {
            "rank": 1,
            "improvement": "<specific improvement>",
            "estimated_ats_boost": "5-10%|10-15%|15-20%|20%+"
        }
    ],
    "industry_specific_notes": "<notes about industry best practices>",
    "overall_feedback": "<2-3 sentences of overall assessment>"
}

CRITICAL RULES:
1. Return ONLY valid JSON - no markdown, code blocks, or explanations
2. All string values must be properly escaped
3. All arrays must contain valid objects/values
4. Do not include backticks or code block markers
5. Ensure all JSON is valid and parseable
6. Do not add any text before or after the JSON object
"""

    return base_prompt


def get_interview_prep_prompt(resume_text: str, role: str = "Software Engineer", level: str = "mid-level") -> str:
    """
    Generate prompt for interview preparation.
    
    Args:
        resume_text (str): Resume content
        role (str): Target job role
        level (str): Experience level
        
    Returns:
        str: Formatted prompt
    """
    
    prompt = f"""Based on this resume, prepare interview guidance for a {level} {role} position.

RESUME:
{resume_text[:3000]}

Return ONLY a valid JSON object with NO additional text:
{{
    "top_talking_points": [
        {{"point": "...", "context": "...", "impact": "..."}}, 
    ],
    "potential_weakness_questions": [
        {{"question": "...", "suggested_response_angle": "..."}}
    ],
    "questions_to_ask": [
        "question1",
        "question2"
    ],
    "preparation_tips": [
        "tip1",
        "tip2",
        "tip3"
    ]
}}

Return ONLY JSON, no other text."""
    
    return prompt
