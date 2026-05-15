from fastapi import FastAPI
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager

from app.database import engine
from app.models import Base
from app.middleware import log_requests
from app.security import RateLimiter
from app.logging_config import setup_logger
from app.routers import (
    auth_router,
    products_router,
    orders_router,
    cart_router,
    wishlist_router,
    coupons_router,
    inventory_router
)

# Initialize Logger
logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and run migrations
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Application Startup Complete")
    yield
    # Shutdown
    logger.info("Application Shutting Down...")

# Initialize App with Lifespan and Middleware
app = FastAPI(
    title="Online Shopping Platform API",
    description="A complete e-commerce API with user authentication, products, cart, orders, and more",
    version="2.0.0",
    lifespan=lifespan,
    middleware=[
        Middleware(log_requests),
        Middleware(RateLimiter, max_requests=10, window_seconds=60) # Limit to 10 reqs/min
    ]
)

# Include routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(cart_router)
app.include_router(wishlist_router)
app.include_router(coupons_router)
app.include_router(inventory_router)

# --- Root endpoint ---
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Online Shopping Platform API"}