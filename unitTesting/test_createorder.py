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


def test_create_order():
    # Place an order
    order_payload = {
        "products": [
            {"product_id": 2633,       #replace product_id with created product_id in database (e.g: 1234)
             "quantity": 2
             }
            ],
        "status": "pending"
    }
    
    order_response = response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 400, f"Unexpected response: {order_response.json()}"

