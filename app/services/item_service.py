from app.models.schemas import ItemCreate
from app.services.dependency_client import get_dependency_data
from app.repositories.item_repository import (
    create_item as repository_create,
    get_items as repository_get_items,
    get_item as repository_get_item,
    update_item as repository_update_item,
    delete_item as repository_delete_item,
)


def create_item(item: ItemCreate):
    item_id = repository_create(
        item.name,
        item.description,
        item.status.value,
    )

    return {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "status": item.status,
    }


def get_items():
    items = repository_get_items()
    dependency_data, dependency_error = get_dependency_data()

    return {
        "items": items,
        "dependency": dependency_data,
        "dependency_error": dependency_error,
    }


def get_item(item_id: int):
    return repository_get_item(item_id)


def update_item(item_id: int, item: ItemCreate):
    return repository_update_item(
        item_id,
        item.name,
        item.description,
        item.status.value,
    )


def delete_item(item_id: int):
    return repository_delete_item(item_id)
