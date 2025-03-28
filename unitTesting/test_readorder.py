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


def test_read_order():
    response = client.get("/orders/")
    assert response.status_code == 200
    
