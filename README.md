# ResumeForge AI

Premium AI-powered resume builder and ATS optimizer designed for hackathon-grade production readiness.

Quick start

1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Create virtualenv and install:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

App routes
- `/` Home
- `/resume` Resume Form
- `/ats` ATS Analyzer

API endpoints (JSON)
- `POST /api/generate_resume`
- `POST /api/analyze_ats`
- `POST /api/skill_gap`
- `POST /api/generate_cover_letter`

PDF Export (server-side)
- Server-side PDF generation uses `pdfkit` and requires the `wkhtmltopdf` binary.
- Install `wkhtmltopdf` on Windows via the installer: https://wkhtmltopdf.org/downloads.html
- Optionally set `WKHTMLTOPDF_PATH` env var if the binary is not on PATH.
- Endpoint: `POST /api/render_resume` with JSON `{ "resume": { ... } }` returns application/pdf

Deployment (recommended paths)

1) Quick Docker + Render (recommended for simplicity):
	- Build and push the image to a registry (GitHub Container Registry or Docker Hub).
	- Create a new web service on Render, point it to the image or connect to GitHub repo and use "Dockerfile" build.
	- Add environment variables in Render: `OPENAI_API_KEY`, `ENV=production`, optionally `WKHTMLTOPDF_PATH`.

2) Google Cloud Run (serverless):
	- Build container and push to Google Container Registry (GCR) or Artifact Registry.
	- Deploy via `gcloud run deploy` specifying `--port=8000` and set env vars.

3) AWS ECS / Fargate or Azure App Service: follow provider docs and deploy the container, expose port 8000, set env vars.

Local Docker test
```bash
docker build -t resumeforge:local .
docker run --env-file .env -p 8000:8000 resumeforge:local
```

GitHub Actions (CI)
- A sample workflow `.github/workflows/ci.yml` is included to build and push the image to `ghcr.io` on pushes to `main`.
- Set repository secrets as needed (none required for GHCR push via `GITHUB_TOKEN`).

Notes about `wkhtmltopdf` in containers
- Some distros' `wkhtmltopdf` may be missing fonts or need additional packages. Test the container locally.
- If wkhtmltopdf is problematic, consider switching to headless Chrome (Puppeteer) or a serverless PDF service.


Notes
- Frontend offers client-side PDF export.
- Prompts are in `app/prompts.py` and AI calls are in `app/services/openai_service.py`.