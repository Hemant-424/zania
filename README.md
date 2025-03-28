# Folder structure

zania/ │── app/ │ ├── routes/ │ │ ├── product.py │ │ ├── order.py │ ├── models/ │ │ ├── product.py │ │ ├── order.py │ ├── database.py │ │── main.py │ │── utility.py │── Testing/ │ ├── test_order.py │ ├── test_product.py │ ├── functiontest.py │ ├── conftest.py │── unitTesting/ │ ├── test_createorder.py │ ├── test_createproduct.py  │ ├── test_readorder.py │ ├── test_readproduct.py│ ├── test_functionTest.py  │── .env │── .gitignore │── Dockerfile │── docker-compose.yml │── requirements.txt │── README.md

__create a .env file, which holds the two env variable__ : MONGO_URI and DB_NAME

# How to run locally
* maintain the above folder structure in code editor
* open terminal in the folder location

* create a virtual environemt in zania folder with command: __python -m venv env_name__

* activate the virtual environemt with command: __env_name/Scripts\activate.bat__

* install the requirements.txt file in virtual environment with command: __pip install -r requirements.txt__

* start the Swagger UI to access the API routes, use : __uvicorn app.main:app --port 8002__

# routes
__Product routes__
* GET /products/ - to get the list of products
* POST /products/ - to create a product
* GET /products/{product_id} - to get a product details
* DELETE /products/{product_id} - to delete a product

__Order routes__
* GET /orders/ - to get the list of order 
* POST /orders/ - to create a order (first create a product)
* GET /orders/{order_id} - to get a order details
* DELETE /orders/{order_id} - to delete a order

# Unit and Integration Test
* Two folders are there, one for Unit Test(folder: unitTesting) and Integration Test (folder: Testing)
__To run the testing, use command from terminal:__  pytest -s -v  (make sure you're inside the venv_name)


# Build docker container and images

* we have two files, Dockerfile and docker-compose.yml
* activate the virtual env in terminal, install the docker extension in VS code
* run the command to build the docker : __docker-compose up --build -d__
* it will create two containers, one for API routes, and another for Unittest and Integration test.
* open the created container , and use the API endpoint from anywhere.


* Note: if you face any issues, I will be happy to guide you. 

__Thank You__
