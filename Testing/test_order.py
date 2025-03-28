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
async def test_create_and_get_order(async_client, mock_db):
    """Test creating and retrieving an order"""
    print("\n")
    print("\n Testing for creating a order and retriving it")
    # Create a product (since an order requires a product)
    product_response = await async_client.post("/products/", json={
        "name": "Test Product Order",
        "description": "Test Description Order",
        "price": 50.0,
        "stock": 3
    })

    assert product_response.status_code == 200
    product_data = product_response.json()
    print("Product is created", product_data)
    product_id = product_data["product_id"]
    # print(product_id)

    # Create an order using the product
    order_response = await async_client.post("/orders/", json={
        "products": [{"product_id": product_id, "quantity": 2}],
        "status": "pending"
    })

    assert order_response.status_code == 200, f"Order created successfully"
    order_data = order_response.json()
    print("Order is created", order_data)
    order_id = order_data["order_id"]

    # Retrieve the created order
    get_response = await async_client.get(f"/orders/{order_id}/")

    assert get_response.status_code == 200
    
    retrieved_order = get_response.json()
    print("order retrieved ", retrieved_order)

    # Validate retrieved order details
    assert retrieved_order["order_id"] == order_id
    assert retrieved_order["status"] == "pending"
    assert retrieved_order["products"][0]["product_id"] == product_id
    assert retrieved_order["products"][0]["quantity"] == 2
    print("Finished")
    print("\n")

@pytest.mark.asyncio
async def test_insufficient_stock_order(async_client, mock_db):
    """Test creating and retrieving an order"""
    print("\n")
    print("\n Testing for order if stock is insufficient and retriving it")
    # Create a product (since an order requires a product)
    product_response = await async_client.post("/products/", json={
        "name": "Test Product Order",
        "description": "Test Description Order",
        "price": 50.0,
        "stock": 0
    })

    assert product_response.status_code == 200
    product_data = product_response.json()
    print("Product is created", product_data)
    product_id = product_data["product_id"]
    # print(product_id)

    # Create an order using the product
    order_response = await async_client.post("/orders/", json={
        "products": [{"product_id": product_id, "quantity": 2}],
        "status": "pending"
    })

    assert order_response.status_code == 400, f"Order is not placed due to insufficient stock of product - { order_response.json()}"
    order_data = order_response.json()
    print("Order is not created", order_data)

    print("Finished")
    print("\n")





@pytest.mark.asyncio
async def test_create_and_delete_order(async_client, mock_db):
    """Test creating and retrieving an order"""
    print("\n")
    print("\n Testing for create a order and delete it")
    # Create a product (since an order requires a product)
    product_response = await async_client.post("/products/", json={
        "name": "Test Product Order",
        "description": "Test Description Order",
        "price": 50.0,
        "stock": 3
    })

    assert product_response.status_code == 200
    product_data = product_response.json()
    print("Product is created", product_data)
    product_id = product_data["product_id"]
    print(product_id)

    # Create an order using the product
    order_response = await async_client.post("/orders/", json={
        "products": [{"product_id": product_id, "quantity": 2}],
        "status": "pending"
    })

    assert order_response.status_code == 200, f"Order created successfully"
    order_data = order_response.json()
    print("Order is created", order_data)
    order_id = order_data["order_id"]

    # delete the created order
    delete_response = await async_client.delete(f"/orders/{order_id}/")
    print("Order deleted for order_id", order_id)
    assert delete_response.status_code == 200 , f"Order deleted: {delete_response.json()}"
    print("Finished")


#pytest -s -v IntegrationTesting/test_order.py --asyncio-mode=auto 