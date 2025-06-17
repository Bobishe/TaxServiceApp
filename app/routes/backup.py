from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.utils.backup import (
    export_table_csv,
    import_table_csv,
    export_sql_dump,
    import_sql_dump,
)
from app.models import Taxpayer, Payment, TaxDeclaration, Accrual, Debt, Inspection

router = APIRouter()


@router.post('/export/csv/{table_name}')
async def export_csv(table_name: str, db: AsyncSession = Depends(get_session)):
    model = {
        'taxpayer': Taxpayer,
        'payment': Payment,
        'declaration': TaxDeclaration,
        'accrual': Accrual,
        'debt': Debt,
        'inspection': Inspection,
    }.get(table_name)
    if not model:
        return Response(status_code=400)
    path = f'exports/{table_name}.csv'
    await export_table_csv(db, model, path)
    with open(path, 'rb') as f:
        data = f.read()
    return Response(data, media_type='text/csv')


@router.post('/import/csv/{table_name}')
async def import_csv_endpoint(
    table_name: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    model = {
        'taxpayer': Taxpayer,
        'payment': Payment,
        'declaration': TaxDeclaration,
        'accrual': Accrual,
        'debt': Debt,
        'inspection': Inspection,
    }.get(table_name)
    if not model:
        return Response(status_code=400)
    path = f'exports/{table_name}.csv'
    with open(path, 'wb') as f:
        f.write(await file.read())
    await import_table_csv(db, model, path)
    return {'status': 'ok'}


@router.post('/export/sql')
async def export_sql():
    path = 'exports/dump.sql'
    export_sql_dump(path)
    with open(path, 'rb') as f:
        data = f.read()
    return Response(data, media_type='application/sql')


@router.post('/import/sql')
async def import_sql(file: UploadFile = File(...)):
    path = 'exports/upload.sql'
    with open(path, 'wb') as f:
        f.write(await file.read())
    import_sql_dump(path)
    return {'status': 'ok'}
