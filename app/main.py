from fastapi import FastAPI
from app.routes import product, order
from app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Initialize database
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Ensure DB initializes
    yield  # Startup complete
    

app = FastAPI(title="Zania", version="1.0",lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes for all modules
app.include_router(product.product_router, prefix="/products", tags=["Products"])
app.include_router(order.order_router, prefix="/orders", tags=["Orders"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Zania"}
