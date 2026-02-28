"""Web routes serving HTML pages and templates."""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/resume", response_class=HTMLResponse)
def resume_form(request: Request):
    return templates.TemplateResponse("resume_form.html", {"request": request})


@router.get("/ats", response_class=HTMLResponse)
def ats_page(request: Request):
    return templates.TemplateResponse("ats_analyzer.html", {"request": request})


@router.get("/results", response_class=HTMLResponse)
def results(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})
