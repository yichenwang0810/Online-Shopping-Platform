from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(Text)
    stock_quantity = Column(Integer, default=0)
    category = Column(String, index=True)
    image_url = Column(String)
    
    # Relationships
    wishlist_items = relationship("WishlistItem", back_populates="product")
    inventory_logs = relationship("InventoryLog", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")