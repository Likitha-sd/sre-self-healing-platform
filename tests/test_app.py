from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_item():
    response = client.post(
        "/api/v1/items",
        json={
            "name": "Test API",
            "description": "API test item",
            "status": "active",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Test API"
    assert data["status"] == "active"
    assert "id" in data


def test_list_items():
    response = client.get("/api/v1/items")
    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "dependency" in data
    assert "dependency_error" in data
    assert isinstance(data["items"], list)

    # The dependency may be unavailable in CI,
    # but the main API should remain available.
    if data["dependency"] is not None:
        assert data["dependency"]["message"] == "Dependency is working"
    else:
        assert data["dependency_error"] in {"unavailable", "circuit_open"}

def test_get_missing_item():
    response = client.get("/api/v1/items/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_invalid_status():
    response = client.post(
        "/api/v1/items",
        json={
            "name": "Invalid",
            "description": "Invalid status test",
            "status": "broken",
        },
    )

    assert response.status_code == 422


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text


def test_empty_name_rejected():
    response = client.post(
        "/api/v1/items",
        json={
            "name": "",
            "description": "Invalid name test",
            "status": "active",
        },
    )

    assert response.status_code == 422


def test_empty_description_rejected():
    response = client.post(
        "/api/v1/items",
        json={
            "name": "Test",
            "description": "",
            "status": "active",
        },
    )

    assert response.status_code == 422


def test_update_item():
    create_response = client.post(
        "/api/v1/items",
        json={
            "name": "Update Test",
            "description": "Before update",
            "status": "active",
        },
    )

    item_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/items/{item_id}",
        json={
            "name": "Updated Item",
            "description": "After update",
            "status": "inactive",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Updated Item"
    assert data["description"] == "After update"
    assert data["status"] == "inactive"


def test_delete_item():
    create_response = client.post(
        "/api/v1/items",
        json={
            "name": "Delete Test",
            "description": "Item to delete",
            "status": "active",
        },
    )

    item_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/items/{item_id}")

    assert response.status_code == 204


def test_deleted_item_not_found():
    create_response = client.post(
        "/api/v1/items",
        json={
            "name": "Delete Verify",
            "description": "Item to delete",
            "status": "active",
        },
    )

    item_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/items/{item_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404
