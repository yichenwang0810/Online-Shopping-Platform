from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    discount_percent = Column(Float)  # e.g., 10.0 for 10%
    is_active = Column(Boolean, default=True)
    usage_limit = Column(Integer, default=None)  # None means unlimited
    used_count = Column(Integer, default=0)