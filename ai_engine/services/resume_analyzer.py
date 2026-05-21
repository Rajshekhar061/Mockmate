"""
Resume analysis prompt templates.
"""


def get_resume_analysis_prompt(resume_text, job_description=None):
    """
    Generate prompt for resume analysis.
    """

    jd_section = ""

    if job_description:
        jd_section = f"""
Target Job Description:
{job_description}
"""

    return f"""
Analyze this resume for ATS optimization and career feedback.

Resume:
{resume_text}

{jd_section}

Return ONLY valid JSON in this exact structure:

{{
    "ats_score": 85,
    "strengths": [
        "Strong technical skills",
        "Good project experience"
    ],
    "weaknesses": [
        "Resume lacks measurable achievements",
        "Formatting can be improved"
    ],
    "suggestions": [
        "Add quantified impact in projects",
        "Improve summary section"
    ],
    "keywords_found": [
        "Python",
        "Django",
        "Machine Learning"
    ],
    "missing_keywords": [
        "Docker",
        "AWS"
    ]
}}

Do not include markdown.
Do not include explanation text.
Return only pure JSON.
"""