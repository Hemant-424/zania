import pytest
from app.database import init_db
from app.main import app
from fastapi.testclient import TestClient
import asyncio


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Ensures the database is initialized before any tests run.
    """
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)  # Set the event loop
    loop.run_until_complete(init_db())  # Run the async DB initialization
    yield  # Yield control back to pytest
    # loop.close()  # Close the event loop after tests are done

client = TestClient(app)


def test_create_product():
    response = client.post("/products/", json={
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "stock": 10
    })
    
    assert response.status_code == 200
    data = response.json()
    # print(data)
    product_id = data.get("product_id")
    assert data["name"] == "Test Product"
    assert data["description"] == "Test Description"
    assert data["price"] == 100.0
    assert data["stock"] == 10


