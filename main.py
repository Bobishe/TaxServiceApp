# main.py
from fastapi import FastAPI
from app.routes import api_router

app = FastAPI(title="АИС «Налог‑Учёт»")

# Register routers
app.include_router(api_router)
