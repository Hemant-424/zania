import pytest
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorClient
from app.utility import generate_unique_id  # Example utility function
from app.database import MONGO_URI


@pytest.mark.asyncio
async def test_generate_unique_id():
    """Test that generate_unique_id returns an integer in a valid range."""
    product_id = generate_unique_id(1000, 9999)
    assert isinstance(product_id, int)
    assert 1000 <= product_id <= 9999

@pytest.mark.asyncio
async def test_database_connection():
    """Test MongoDB connection."""
    # MONGO_URI = "mongodb://localhost:27017"
    client = AsyncIOMotorClient(MONGO_URI)

    try:
        await client.admin.command("ping")
    except Exception:
        pytest.fail("Database connection failed!")