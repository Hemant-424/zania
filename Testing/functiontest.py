import pytest
from app.database import get_db
from motor.motor_asyncio import AsyncIOMotorClient
from app.utility import generate_unique_id 
from app.database import MONGO_URI


@pytest.mark.asyncio
async def test_generate_unique_id():
    #Test that generate_unique_id returns an integer in a valid range.
    print("\n Test the generate_unique_id function")
    product_id = generate_unique_id(1000, 9999)
    assert isinstance(product_id, int)
    assert 1000 <= product_id <= 9999
    print("Finished")

@pytest.mark.asyncio
async def test_database_connection():
    #Test MongoDB connection.
    # MONGO_URI = "mongodb://localhost:27017"
    print("\n Test for database connection")
    client = AsyncIOMotorClient(MONGO_URI)
    try:
        await client.admin.command("ping")
    except Exception:
        pytest.fail("Database connection failed!")
    
    print("Finished")