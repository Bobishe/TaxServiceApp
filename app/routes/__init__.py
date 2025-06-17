from fastapi import APIRouter
from . import taxpayers, declarations, payments

api_router = APIRouter()
api_router.include_router(taxpayers.router, prefix='/taxpayers', tags=['Taxpayers'])
api_router.include_router(declarations.router, prefix='/declarations', tags=['Declarations'])
api_router.include_router(payments.router, prefix='/payments', tags=['Payments'])

__all__ = ['api_router']
