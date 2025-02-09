from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import time

# Templates setup
base_dir = Path(__file__).resolve().parent.parent.parent
templates_dir = base_dir / "api" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Define the router
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    version = time.time()
    return templates.TemplateResponse(
        "base.html", {"request": request, "version": version}
    )