# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import api_router

app = FastAPI(title="АИС «Налог‑Учёт»")

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register routers
app.include_router(api_router)
