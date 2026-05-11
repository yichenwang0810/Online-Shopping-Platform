# exceptions.py
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

# Custom Error Classes
class OutOfStockError(Exception):
    """Raised when a product is out of stock"""
    pass

class PaymentFailedError(Exception):
    """Raised when payment processing fails"""
    pass

# Exception Handlers to register with FastAPI
async def out_of_stock_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "One or more items in your cart are out of stock."}
    )

async def generic_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."}
    )