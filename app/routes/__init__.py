from fastapi import APIRouter
from . import (
    taxpayers,
    declarations,
    payments,
    debts,
    inspections,
    reports,
    backup,
    web,
)

api_router = APIRouter()

# Mount API endpoints under /api to avoid conflicts with HTML routes
api_router.include_router(taxpayers.router, prefix="/api/taxpayers", tags=["Taxpayers"])
api_router.include_router(
    declarations.router, prefix="/api/declarations", tags=["Declarations"]
)
api_router.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
api_router.include_router(debts.router, prefix="/api/debts", tags=["Debts"])
api_router.include_router(
    inspections.router, prefix="/api/inspections", tags=["Inspections"]
)
api_router.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
api_router.include_router(backup.router, prefix="/api/backup", tags=["Backup"])

# Web interface routes remain without the /api prefix
api_router.include_router(web.router, prefix="", tags=["Web"])

__all__ = ["api_router"]
