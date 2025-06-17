from .taxpayer import (
    get_taxpayer,
    search_taxpayers,
    create_taxpayer,
    update_taxpayer,
)
from .declaration import get_declaration, create_declaration
from .payment import get_payment, create_payment
from .debt import calculate_debts
from .inspection import get_inspection, list_inspections, create_inspection
from .report import tax_revenue_report, debtors_list

__all__ = [
    'get_taxpayer',
    'search_taxpayers',
    'create_taxpayer',
    'update_taxpayer',
    'get_declaration',
    'create_declaration',
    'get_payment',
    'create_payment',
    'calculate_debts',
    'get_inspection',
    'list_inspections',
    'create_inspection',
    'tax_revenue_report',
    'debtors_list',
]
