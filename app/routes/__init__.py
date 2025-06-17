from fastapi import APIRouter
from . import taxpayers, declarations, payments, debts, inspections, reports, backup

api_router = APIRouter()
api_router.include_router(taxpayers.router, prefix='/taxpayers', tags=['Taxpayers'])
api_router.include_router(declarations.router, prefix='/declarations', tags=['Declarations'])
api_router.include_router(payments.router, prefix='/payments', tags=['Payments'])
api_router.include_router(debts.router, prefix='/debts', tags=['Debts'])
api_router.include_router(inspections.router, prefix='/inspections', tags=['Inspections'])
api_router.include_router(reports.router, prefix='/reports', tags=['Reports'])
api_router.include_router(backup.router, prefix='/backup', tags=['Backup'])

__all__ = ['api_router']
