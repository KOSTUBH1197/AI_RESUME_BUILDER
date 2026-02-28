"""High-level AI service functions that implement the product features using prompts and the OpenAI wrapper."""
from typing import Dict, Any
from app.prompts import PROMPTS
from app.services.openai_service import call_chat


def generate_resume(structured_input: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a professional resume JSON from structured form input.

    structured_input should be a dict with keys like name, contact, summary, experience, education, projects, skills
    """
    prompt_user = PROMPTS["resume_generation"]["user"].format(input_json=structured_input)
    return call_chat(PROMPTS["resume_generation"]["system"], prompt_user, max_tokens=900)


def analyze_ats(job: str, resume_text: str) -> Dict[str, Any]:
    prompt_user = PROMPTS["ats_analysis"]["user"].format(job=job, resume=resume_text)
    return call_chat(PROMPTS["ats_analysis"]["system"], prompt_user, max_tokens=600)


def skill_gap_analysis(job: str, resume_text: str) -> Dict[str, Any]:
    prompt_user = PROMPTS["skill_gap"]["user"].format(job=job, resume=resume_text)
    return call_chat(PROMPTS["skill_gap"]["system"], prompt_user, max_tokens=500)


def generate_cover_letter(company: str, role: str, resume_summary: str) -> Dict[str, Any]:
    prompt_user = PROMPTS["cover_letter"]["user"].format(company=company, role=role, summary=resume_summary)
    return call_chat(PROMPTS["cover_letter"]["system"], prompt_user, max_tokens=350)
