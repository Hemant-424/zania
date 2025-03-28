import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")



db_client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None

async def init_db():
    """Initialize the database connection"""
    global db_client, database
    db_client = AsyncIOMotorClient(MONGO_URI)
    database = db_client[DB_NAME]

async def close_db():
    """Close the database connection"""
    global db_client
    if db_client:
        db_client.close()

def get_db() -> AsyncIOMotorDatabase:
    """Retrieve the database instance"""
    if database is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return database

