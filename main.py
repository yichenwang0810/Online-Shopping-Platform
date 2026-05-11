# main.py
from fastapi import FastAPI
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager

import models, database
from middleware import log_requests
from security import RateLimiter
from logging_config import setup_logger

# Initialize Logger
logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run migrations
    logger.info("Running database migrations...")
    import migrations
    migrations.run_migrations()
    logger.info("Application Startup Complete")
    yield
    # Shutdown
    logger.info("Application Shutting Down...")

# Initialize App with Lifespan and Middleware
app = FastAPI(
    title="Shop API v4.0", 
    lifespan=lifespan,
    middleware=[
        Middleware(log_requests),
        Middleware(RateLimiter, max_requests=10, window_seconds=60) # Limit to 10 reqs/min
    ]
)

# --- Routes (Simplified for brevity) ---
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Shop API"}