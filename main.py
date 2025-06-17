# main.py
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import api_router

app = FastAPI(title="АИС «Налог‑Учёт»")

# Serve static UI
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def ui_index():
    """Serve the simple Bootstrap-based UI."""
    return FileResponse("app/static/index.html")

# Register routers
app.include_router(api_router)
