"""
Application entrypoint - FastAPI app configured with Jinja2 templates and routes.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes.web import router as web_router
from app.routes.api import router as api_router
from app.config import settings

app = FastAPI(title="ResumeForge AI")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(web_router)
app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print(f"Starting ResumeForge AI on {settings.APP_HOST}:{settings.APP_PORT}")
