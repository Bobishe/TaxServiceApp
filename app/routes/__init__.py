from fastapi import APIRouter
from . import taxpayers

api_router = APIRouter()
api_router.include_router(taxpayers.router, prefix='/taxpayers', tags=['Taxpayers'])

__all__ = ['api_router']
