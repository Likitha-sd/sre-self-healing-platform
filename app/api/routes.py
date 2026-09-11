from fastapi import APIRouter, HTTPException
from app.models.schemas import Item, ItemCreate, ItemListResponse
from app.services.item_service import (
    create_item,
    get_items,
    get_item,
    update_item,
    delete_item,
)

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.post("", response_model=Item, status_code=201)
def create(item: ItemCreate):
    return create_item(item)


@router.get("", response_model=ItemListResponse)
def list_items():
    return get_items()


@router.get("/{item_id}", response_model=Item)
def get(item_id: int):
    item = get_item(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put("/{item_id}", response_model=Item)
def update(item_id: int, item: ItemCreate):
    updated = update_item(item_id, item)

    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated


@router.delete("/{item_id}", status_code=204)
def remove(item_id: int):
    if not delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
