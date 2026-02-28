"""JSON API endpoints consumed by the frontend (AJAX)."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.services.ai_service import generate_resume, analyze_ats, skill_gap_analysis, generate_cover_letter
import pdfkit
import io
import os

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


class ResumeInput(BaseModel):
    header: dict
    summary: str
    experience: list
    education: list
    projects: list
    skills: list


class ATSInput(BaseModel):
    job_description: str
    resume_text: str


class SkillGapInput(BaseModel):
    job_description: str
    resume_text: str


class CoverLetterInput(BaseModel):
    company: str
    role: str
    resume_summary: str


class RenderInput(BaseModel):
    # Accept resume structured JSON to render
    resume: dict


@router.post("/generate_resume")
def api_generate_resume(payload: ResumeInput):
    result = generate_resume(payload.dict())
    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])
    return result


@router.post("/analyze_ats")
def api_analyze_ats(payload: ATSInput):
    result = analyze_ats(payload.job_description, payload.resume_text)
    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])
    return result


@router.post("/skill_gap")
def api_skill_gap(payload: SkillGapInput):
    result = skill_gap_analysis(payload.job_description, payload.resume_text)
    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])
    return result


@router.post("/generate_cover_letter")
def api_generate_cover_letter(payload: CoverLetterInput):
    result = generate_cover_letter(payload.company, payload.role, payload.resume_summary)
    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])
    return result


@router.post("/render_resume")
def api_render_resume(payload: RenderInput):
    """Render the provided resume JSON to PDF using wkhtmltopdf via pdfkit.

    Requires `wkhtmltopdf` binary installed on the host. Optionally set `WKHTMLTOPDF_PATH` env var.
    """
    try:
        # Render HTML using template
        html = templates.env.get_template("resume_template.html").render(resume=payload.resume)

        wkpath = os.getenv("WKHTMLTOPDF_PATH")
        config = None
        if wkpath:
            config = pdfkit.configuration(wkhtmltopdf=wkpath)

        options = {
            "enable-local-file-access": None,
            "quiet": "",
        }

        pdf_bytes = pdfkit.from_string(html, False, options=options, configuration=config)
        return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=resume.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
