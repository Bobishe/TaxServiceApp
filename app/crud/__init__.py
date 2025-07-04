from .taxpayer import (
    get_taxpayer,
    search_taxpayers,
    count_taxpayers,
    create_taxpayer,
    update_taxpayer,
    autocomplete_taxpayers,
)
from .declaration import (
    get_declaration,
    create_declaration,
    search_declarations,
    count_declarations,
    list_declarations_by_taxpayer,
)
from .payment import (
    get_payment,
    create_payment,
    search_payments,
    count_payments,
)
from .debt import calculate_debts, get_total_debt
from .inspection import get_inspection, list_inspections, create_inspection
from .report import tax_revenue_report, debtors_list
from .taxtype import list_tax_types

__all__ = [
    "get_taxpayer",
    "search_taxpayers",
    "count_taxpayers",
    "create_taxpayer",
    "update_taxpayer",
    "autocomplete_taxpayers",
    "get_declaration",
    "create_declaration",
    "search_declarations",
    "count_declarations",
    "list_declarations_by_taxpayer",
    "get_payment",
    "create_payment",
    "search_payments",
    "count_payments",
    "calculate_debts",
    "get_total_debt",
    "get_inspection",
    "list_inspections",
    "create_inspection",
    "tax_revenue_report",
    "debtors_list",
    "list_tax_types",
]
