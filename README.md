# Online Shopping Platform

A complete e-commerce platform built with FastAPI, featuring user authentication, product management, shopping cart, order processing, and more.

## Features

- **User Authentication**: Register, login, and JWT-based authentication
- **Product Management**: CRUD operations for products (admin only)
- **Shopping Cart**: Add/remove items, persistent cart storage
- **Order Management**: Place orders, view order history
- **Wishlist**: Save favorite products
- **Coupons**: Apply discount codes to purchases
- **Inventory Tracking**: Monitor stock levels and changes
- **Admin Panel**: Administrative features for managing the platform
- **Responsive Frontend**: Modern web interface with authentication

## Project Structure

```
online-shopping-platform/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── config.py            # Application settings
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   ├── repositories/        # Data access layer
│   ├── dependencies/        # FastAPI dependencies
│   ├── middleware/          # Custom middleware
│   ├── security/            # Authentication utilities
│   └── logging_config.py    # Logging configuration
├── static/                  # Static files (CSS, JS)
├── templates/               # Jinja2 templates
├── tests/                   # Unit and integration tests
├── migrations.py            # Database migrations
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/online-shopping-platform.git
cd online-shopping-platform
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000` and the frontend at `http://127.0.0.1:8000/index.html`.

## API Documentation

Once the application is running, visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Key Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Products
- `GET /products` - List all products
- `GET /products/{id}` - Get product details
- `POST /products` - Create product (admin only)
- `PUT /products/{id}` - Update product (admin only)
- `DELETE /products/{id}` - Delete product (admin only)

### Cart
- `GET /cart` - Get user's cart
- `POST /cart/items` - Add item to cart
- `PUT /cart/items/{product_id}` - Update cart item
- `DELETE /cart/items/{product_id}` - Remove item from cart

### Orders
- `GET /orders` - Get user's orders
- `POST /orders` - Create new order
- `GET /orders/{id}` - Get order details

### Wishlist
- `GET /wishlist` - Get user's wishlist
- `POST /wishlist` - Add product to wishlist
- `DELETE /wishlist/{product_id}` - Remove from wishlist

### Coupons
- `POST /coupons/apply` - Apply coupon code
- `POST /coupons` - Create coupon (admin only)

## Database

The application uses SQLite by default. To initialize the database:

```bash
python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

## Testing

Run tests with pytest:

```bash
pytest
```

## Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
