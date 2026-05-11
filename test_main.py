# test_main.py
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app # Import the app from main.py

# Setup a test database (SQLite in memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_read_products():
    """Test that we can fetch the product list"""
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_order_validation():
    """Test that the API rejects invalid orders (e.g., negative quantity)"""
    order_data = {"items": [{"product_id": 999, "quantity": -5}]}
    response = client.post("/api/orders", json=order_data)
    # We expect a 422 Unprocessable Entity because of Pydantic validation
    assert response.status_code == 422 