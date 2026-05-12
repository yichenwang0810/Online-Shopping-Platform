# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Relationships
    wishlist = relationship("WishlistItem", back_populates="owner")
    orders = relationship("Order", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    stock_quantity = Column(Integer, default=0)
    
    # Relationships
    wishlist_items = relationship("WishlistItem", back_populates="product")
    inventory_logs = relationship("InventoryLog", back_populates="product")

class WishlistItem(Base):
    __tablename__ = "wishlist"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    owner = relationship("User", back_populates="wishlist")
    product = relationship("Product", back_populates="wishlist_items")

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    discount_percent = Column(Float) # e.g., 10.0 for 10%
    is_active = Column(Boolean, default=True)

class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    change_amount = Column(Integer) # +5 or -2
    reason = Column(String) # "Order #123", "Restock", "Damaged"
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="inventory_logs")