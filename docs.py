# docs.py
# Centralized documentation strings for the API

PRODUCT_TAGS = ["Products"]
ORDER_TAGS = ["Orders"]

PRODUCT_DESCRIPTIONS = {
    "get_products": "Retrieve a list of all available products in the store.",
    "create_product": "Add a new product to the inventory. Requires admin privileges."
}

ORDER_DESCRIPTIONS = {
    "create_order": "Place a new order. This calculates the total price and reserves stock."
}