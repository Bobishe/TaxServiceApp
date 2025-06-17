from .taxpayer import (
    get_taxpayer,
    search_taxpayers,
    create_taxpayer,
    update_taxpayer,
)
from .declaration import get_declaration, create_declaration
from .payment import get_payment, create_payment

__all__ = [
    'get_taxpayer',
    'search_taxpayers',
    'create_taxpayer',
    'update_taxpayer',
    'get_declaration',
    'create_declaration',
    'get_payment',
    'create_payment',
]
