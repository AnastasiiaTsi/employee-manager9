from fastapi.testclient import TestClient
from employee_manager.api import app
import pytest

client = TestClient(app)

def test_create_employee(session_override):
    response = client.post("/employees", json={
        "name": "Anna Koval", "position": "Developer",
        "salary": 25000, "department_id": 1
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Anna Koval"

def test_invalid_salary(session_override):
    response = client.post("/employees", json={
        "name": "Anna", "position": "Dev", "salary": -1, "department_id": 1
    })
    assert response.status_code == 422

def test_get_nonexistent_employee(session_override):
    response = client.get("/employees/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_async_batch_statistics():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        response = await async_client.post("/departments/batch-statistics", json=[1])
        assert response.status_code in (200, 504)