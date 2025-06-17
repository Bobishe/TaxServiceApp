from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud import (
    search_taxpayers,
    count_taxpayers,
    get_taxpayer,
    create_taxpayer as crud_create_taxpayer,
    update_taxpayer as crud_update_taxpayer,
    create_declaration as crud_create_declaration,
    search_declarations,
    count_declarations,
    list_tax_types,
    get_total_debt,
)
from app.schemas import TaxpayerCreate, TaxpayerUpdate, TaxDeclarationCreate

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", name="web.index")
async def index(request: Request):
    url = router.url_path_for("web.list_taxpayers")
    return RedirectResponse(url)


@router.get("/taxpayers", name="web.list_taxpayers")
async def list_taxpayers(
    request: Request,
    query: str = "",
    page: int = 1,
    db: AsyncSession = Depends(get_session),
):
    limit = 20
    offset = (page - 1) * limit
    total = await count_taxpayers(db, query)
    taxpayers = await search_taxpayers(db, query, limit=limit, offset=offset)

    # Calculate total debt for each taxpayer
    debt_map = {}
    for tp in taxpayers:
        debt_map[tp.taxpayer_id] = await get_total_debt(db, tp.taxpayer_id)

    pages = (total + limit - 1) // limit
    return templates.TemplateResponse(
        "taxpayers/list.html",
        {
            "request": request,
            "taxpayers": taxpayers,
            "debt_map": debt_map,
            "query": query,
            "page": page,
            "pages": pages,
            "active_tab": "taxpayers",
        },
    )


@router.get("/taxpayers/new", name="web.new_taxpayer")
async def new_taxpayer_form(request: Request):
    return templates.TemplateResponse(
        "taxpayers/form.html",
        {
            "request": request,
            "taxpayer": {},
            "new": True,
            "active_tab": "taxpayers",
        },
    )


@router.post("/taxpayers/new")
async def create_taxpayer(
    request: Request,
    taxpayer_id: str = Form(...),
    type: str = Form(...),
    last_name: str = Form(""),
    first_name: str = Form(""),
    middle_name: str = Form(""),
    company_name: str = Form(""),
    ogrn: str = Form(""),
    region_code: str = Form(""),
    city: str = Form(""),
    street: str = Form(""),
    house: str = Form(""),
    apartment: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    db: AsyncSession = Depends(get_session),
):
    data = TaxpayerCreate(
        taxpayer_id=taxpayer_id,
        type=type,
        last_name=last_name or None,
        first_name=first_name or None,
        middle_name=middle_name or None,
        company_name=company_name or None,
        ogrn=ogrn or None,
        region_code=int(region_code) if region_code else None,
        city=city or None,
        street=street or None,
        house=house or None,
        apartment=apartment or None,
        phone=phone or None,
        email=email or None,
    )
    await crud_create_taxpayer(db, data.dict())
    url = router.url_path_for("web.list_taxpayers")
    return RedirectResponse(url, status_code=303)


@router.get("/taxpayers/{taxpayer_id}", name="web.edit_taxpayer")
async def edit_taxpayer(
    request: Request, taxpayer_id: str, db: AsyncSession = Depends(get_session)
):
    tp = await get_taxpayer(db, taxpayer_id)
    if not tp:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    return templates.TemplateResponse(
        "taxpayers/form.html",
        {
            "request": request,
            "taxpayer": tp,
            "new": False,
            "active_tab": "taxpayers",
        },
    )


@router.post("/taxpayers/{taxpayer_id}")
async def update_taxpayer(
    request: Request,
    taxpayer_id: str,
    type: str = Form(...),
    last_name: str = Form(""),
    first_name: str = Form(""),
    middle_name: str = Form(""),
    company_name: str = Form(""),
    ogrn: str = Form(""),
    region_code: str = Form(""),
    city: str = Form(""),
    street: str = Form(""),
    house: str = Form(""),
    apartment: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    db: AsyncSession = Depends(get_session),
):
    tp = await get_taxpayer(db, taxpayer_id)
    if not tp:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    data = TaxpayerUpdate(
        type=type,
        last_name=last_name or None,
        first_name=first_name or None,
        middle_name=middle_name or None,
        company_name=company_name or None,
        ogrn=ogrn or None,
        region_code=int(region_code) if region_code else None,
        city=city or None,
        street=street or None,
        house=house or None,
        apartment=apartment or None,
        phone=phone or None,
        email=email or None,
    )
    await crud_update_taxpayer(db, tp, data.dict(exclude_unset=True))
    url = router.url_path_for("web.edit_taxpayer", taxpayer_id=taxpayer_id)
    return RedirectResponse(url, status_code=303)


@router.get("/declarations", name="web.list_declarations")
async def list_declarations(
    request: Request,
    query: str = "",
    page: int = 1,
    db: AsyncSession = Depends(get_session),
):
    limit = 20
    offset = (page - 1) * limit
    total = await count_declarations(db, query)
    declarations = await search_declarations(db, query, limit=limit, offset=offset)
    pages = (total + limit - 1) // limit
    return templates.TemplateResponse(
        "declarations/list.html",
        {
            "request": request,
            "declarations": declarations,
            "query": query,
            "page": page,
            "pages": pages,
            "active_tab": "declarations",
        },
    )


@router.get("/declarations/new", name="web.add_declaration")
async def new_declaration_form(
    request: Request,
    taxpayer_id: str = "",
    db: AsyncSession = Depends(get_session),
):
    tax_types = await list_tax_types(db)

    context = {
        "request": request,
        "active_tab": "declarations",
        "tax_types": tax_types,
    }
    if taxpayer_id:
        context["taxpayer"] = {"taxpayer_id": taxpayer_id}
    return templates.TemplateResponse("declarations/form.html", context)


@router.post("/declarations/new")
async def create_declaration(
    request: Request,
    taxpayer_id: str = Form(...),
    tax_type_id: str = Form(...),
    period: int = Form(...),
    submission_date: str = Form(...),
    declared_tax_amount: float = Form(...),
    db: AsyncSession = Depends(get_session),
):
    data = TaxDeclarationCreate(
        taxpayer_id=taxpayer_id,
        tax_type_id=tax_type_id,
        period=period,
        submission_date=submission_date,
        declared_tax_amount=declared_tax_amount,
    )
    await crud_create_declaration(db, data.dict())
    url = router.url_path_for("web.edit_taxpayer", taxpayer_id=taxpayer_id)
    return RedirectResponse(url, status_code=303)
