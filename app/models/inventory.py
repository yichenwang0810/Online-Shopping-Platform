from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    change_amount = Column(Integer)  # +5 or -2
    reason = Column(String)  # "Order #123", "Restock", "Damaged"
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="inventory_logs")