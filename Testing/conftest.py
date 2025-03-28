import pytest
import mongomock
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import get_db
from app.main import app
import mongomock_motor
import pytest_asyncio

# Mock MongoDB setup
@pytest_asyncio.fixture(scope="function")
async def mock_db():
    """Create a mock MongoDB instance."""
    client = mongomock_motor.AsyncMongoMockClient()  # Creates a fake MongoDB client
    db = client["test_db"]
    app.dependency_overrides[get_db] = lambda: db  # Override FastAPI's dependency
    yield db  # Provide db instance to the test
    client.close()
