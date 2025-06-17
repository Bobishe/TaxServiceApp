from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import tax_revenue_report, debtors_list
from app.schemas import TaxRevenueItem, DebtorItem
from app.utils.reporting import generate_pdf, generate_excel

router = APIRouter()


@router.get('/payments', response_model=List[TaxRevenueItem])
async def payments_report(db: AsyncSession = Depends(get_session)):
    return await tax_revenue_report(db)


@router.get('/payments/pdf')
async def payments_report_pdf(db: AsyncSession = Depends(get_session)):
    data = await tax_revenue_report(db)
    pdf_bytes = generate_pdf(data, 'Tax Revenue Report')
    return Response(pdf_bytes, media_type='application/pdf')


@router.get('/payments/excel')
async def payments_report_excel(db: AsyncSession = Depends(get_session)):
    data = await tax_revenue_report(db)
    xls_bytes = generate_excel(data, 'Tax Revenue Report')
    return Response(xls_bytes, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@router.get('/debtors', response_model=List[DebtorItem])
async def debtors_report(db: AsyncSession = Depends(get_session)):
    return await debtors_list(db)


@router.get('/debtors/pdf')
async def debtors_report_pdf(db: AsyncSession = Depends(get_session)):
    data = await debtors_list(db)
    pdf_bytes = generate_pdf(data, 'Debtors List')
    return Response(pdf_bytes, media_type='application/pdf')


@router.get('/debtors/excel')
async def debtors_report_excel(db: AsyncSession = Depends(get_session)):
    data = await debtors_list(db)
    xls_bytes = generate_excel(data, 'Debtors List')
    return Response(xls_bytes, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
