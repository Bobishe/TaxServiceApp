from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import get_declaration, create_declaration
from app.schemas import TaxDeclarationCreate, TaxDeclarationRead

router = APIRouter()


@router.post('/', response_model=TaxDeclarationRead)
async def create(decl: TaxDeclarationCreate, db: AsyncSession = Depends(get_session)):
    return await create_declaration(db, decl.dict())


@router.get('/{declaration_id}', response_model=TaxDeclarationRead)
async def read(declaration_id: int, db: AsyncSession = Depends(get_session)):
    declaration = await get_declaration(db, declaration_id)
    if not declaration:
        raise HTTPException(status_code=404, detail='Declaration not found')
    return declaration
