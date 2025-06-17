# main.py
from fastapi import FastAPI
# from app.routes import taxpayers, declarations, payments  # будете добавлять

app = FastAPI(title="АИС «Налог‑Учёт»")

# Регистрируем роутеры
# app.include_router(taxpayers.router, prefix="/taxpayers", tags=["Taxpayers"])
# app.include_router(declarations.router, prefix="/declarations", tags=["Declarations"])
# app.include_router(payments.router, prefix="/payments", tags=["Payments"])
