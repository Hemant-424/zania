import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import pytest_asyncio

@pytest_asyncio.fixture
async def async_client():
    """Create an async test client with ASGITransport."""
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_product(async_client, mock_db):
    """Unit Test product creation using MockMongo"""
    print("\n Testing for creating a product")
    product_response = await async_client.post("/products/", json={
        "name": "Test Order Product",
        "description": "For testing orders",
        "price": 50.0,
        "stock": 5
    })
    print("Testing for creating product")
    assert product_response.status_code == 200
    data = product_response.json()
    print("Product created ", data)
    assert "product_id" in data
    assert data["name"] == "Test Order Product"
    return data["product_id"]  # Needed for the next test
    print("Finished")



@pytest.mark.asyncio
async def test_create_and_get_product(async_client, mock_db):
    """Test retrieving a product"""
    print("\n Testing for Creating product and retriving product data")
    product_response = await async_client.post("/products/", json={
        "name": "Test Order Product",
        "description": "For testing orders",
        "price": 50.0,
        "stock": 5
    })

    assert product_response.status_code == 200
    data = product_response.json()
    print("Product created ", data)
    product_id = data["product_id"]
    assert "product_id" in data
    assert data["name"] == "Test Order Product"
    return data["product_id"]  # Needed for the next test

    #test product
    get_response = await async_client.get(f"/products/{product_id}/")
    assert get_response.status_code == 200
    retrieved_product = get_response.json()
    print("product retrived ",retrieved_product)
    assert retrieved_product["name"] == "Test Order Product"
    print("Finished")
    


@pytest.mark.asyncio
async def test_create_and_delete_product(async_client, mock_db):
    """Test deleting a product"""
    print("\n Testing for creating product and deleting it")
    product_response = await async_client.post("/products/", json={
        "name": "Test Order Product1",
        "description": "For testing orders",
        "price": 50.0,
        "stock": 5
    })

    assert product_response.status_code == 200
    data = product_response.json()
    product_id = data["product_id"]
    print("Product created ", data)
    delete_response = await async_client.delete(f"/products/{product_id}/")
    print("Product deleted for product_id", product_id)
    assert delete_response.status_code == 200, f"Product deleted: {delete_response.json()}"

    print("Finished")


