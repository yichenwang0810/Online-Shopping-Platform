from .auth import router as auth_router
from .products import router as products_router
from .orders import router as orders_router
from .cart import router as cart_router
from .wishlist import router as wishlist_router
from .coupons import router as coupons_router
from .inventory import router as inventory_router

__all__ = [
    "auth_router",
    "products_router",
    "orders_router",
    "cart_router",
    "wishlist_router",
    "coupons_router",
    "inventory_router"
]