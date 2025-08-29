"""
Legacy routes for the Interview Trainer API.

This module contains legacy endpoints for backward compatibility.
These endpoints are kept to maintain compatibility with existing clients.
"""

from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["legacy"])


# Legacy schemas (keeping for backward compatibility)
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """Legacy endpoint for reading items"""
    return {"item_id": item_id, "q": q}


@router.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Legacy endpoint for updating items"""
    return {"item_name": item.name, "item_id": item_id}
