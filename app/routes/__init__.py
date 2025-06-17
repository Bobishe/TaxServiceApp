from fastapi import APIRouter
from . import taxpayers, declarations, payments, debts, inspections

api_router = APIRouter()
api_router.include_router(taxpayers.router, prefix='/taxpayers', tags=['Taxpayers'])
api_router.include_router(declarations.router, prefix='/declarations', tags=['Declarations'])
api_router.include_router(payments.router, prefix='/payments', tags=['Payments'])
api_router.include_router(debts.router, prefix='/debts', tags=['Debts'])
api_router.include_router(inspections.router, prefix='/inspections', tags=['Inspections'])

__all__ = ['api_router']
