// static/js/app.js
const API_URL = 'http://127.0.0.1:8000';
let currentUser = null;
let token = localStorage.getItem('token');

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        // Try to validate token
        fetch(`${API_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => response.json())
        .then(user => {
            currentUser = user;
            showAuthenticatedUI();
        })
        .catch(() => {
            localStorage.removeItem('token');
            token = null;
            showUnauthenticatedUI();
        });
    } else {
        showUnauthenticatedUI();
    }
    loadProducts();
});

function showAuthenticatedUI() {
    document.getElementById('login-btn').style.display = 'none';
    document.getElementById('register-btn').style.display = 'none';
    document.getElementById('logout-btn').style.display = 'inline';
    document.getElementById('user-info').textContent = `Welcome, ${currentUser.username}!`;
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('cart-section').style.display = 'block';
    document.getElementById('orders-section').style.display = 'block';
    loadCart();
    loadOrders();
}

function showUnauthenticatedUI() {
    document.getElementById('login-btn').style.display = 'inline';
    document.getElementById('register-btn').style.display = 'inline';
    document.getElementById('logout-btn').style.display = 'none';
    document.getElementById('user-info').textContent = '';
    document.getElementById('cart-section').style.display = 'none';
    document.getElementById('orders-section').style.display = 'none';
}

function showLogin() {
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('register-form').style.display = 'none';
}

function showRegister() {
    document.getElementById('auth-section').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (response.ok) {
            token = data.access_token;
            localStorage.setItem('token', token);
            // Get user info
            const userResponse = await fetch(`${API_URL}/auth/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            currentUser = await userResponse.json();
            showAuthenticatedUI();
            document.getElementById('login-message').textContent = '';
        } else {
            document.getElementById('login-message').textContent = data.detail || 'Login failed';
        }
    } catch (error) {
        document.getElementById('login-message').textContent = 'Login failed';
    }
}

async function register() {
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById('register-message').textContent = 'Registration successful! Please login.';
            showLogin();
        } else {
            document.getElementById('register-message').textContent = data.detail || 'Registration failed';
        }
    } catch (error) {
        document.getElementById('register-message').textContent = 'Registration failed';
    }
}

function logout() {
    localStorage.removeItem('token');
    token = null;
    currentUser = null;
    showUnauthenticatedUI();
}

// Fetch and display products
async function loadProducts() {
    try {
        const response = await fetch(`${API_URL}/products`);
        const products = await response.json();
        const container = document.getElementById('products-container');
        container.innerHTML = products.map(p => `
            <div class="product">
                <h2>${p.name}</h2>
                <p>${p.description}</p>
                <p><strong>Price: $${p.price.toFixed(2)}</strong></p>
                <p>Stock: ${p.stock_quantity}</p>
                ${currentUser ? `<button onclick="addToCart(${p.id})">Add to Cart</button>` : ''}
            </div>
        `).join('');
    } catch (error) {
        document.getElementById('products-container').innerText = 'Failed to load products.';
        console.error(error);
    }
}

async function addToCart(productId) {
    if (!token) return;

    try {
        const response = await fetch(`${API_URL}/cart/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ product_id: productId, quantity: 1 })
        });
        if (response.ok) {
            loadCart();
        }
    } catch (error) {
        console.error('Failed to add to cart:', error);
    }
}

async function loadCart() {
    if (!token) return;

    try {
        const response = await fetch(`${API_URL}/cart`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const cart = await response.json();
        const container = document.getElementById('cart-container');
        container.innerHTML = `
            <h3>Total: $${cart.total.toFixed(2)}</h3>
            ${cart.items.map(item => `
                <div class="cart-item">
                    <span>${item.product.name} (x${item.quantity})</span>
                    <span>$${item.subtotal.toFixed(2)}</span>
                    <button onclick="removeFromCart(${item.product.id})">Remove</button>
                </div>
            `).join('')}
        `;
    } catch (error) {
        console.error('Failed to load cart:', error);
    }
}

async function removeFromCart(productId) {
    if (!token) return;

    try {
        await fetch(`${API_URL}/cart/items/${productId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        loadCart();
    } catch (error) {
        console.error('Failed to remove from cart:', error);
    }
}

async function checkout() {
    if (!token) return;

    try {
        // Get cart items
        const cartResponse = await fetch(`${API_URL}/cart`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const cart = await cartResponse.json();

        // Create order
        const items = cart.items.map(item => ({
            product_id: item.product.id,
            quantity: item.quantity
        }));

        const orderResponse = await fetch(`${API_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ items })
        });

        if (orderResponse.ok) {
            alert('Order placed successfully!');
            loadCart();
            loadOrders();
        }
    } catch (error) {
        console.error('Checkout failed:', error);
    }
}

async function loadOrders() {
    if (!token) return;

    try {
        const response = await fetch(`${API_URL}/orders`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const orders = await response.json();
        const container = document.getElementById('orders-container');
        container.innerHTML = orders.map(order => `
            <div class="order">
                <h4>Order #${order.id} - $${order.total_price.toFixed(2)} (${order.status})</h4>
                <p>Ordered on: ${new Date(order.created_at).toLocaleDateString()}</p>
                <ul>
                    ${order.items.map(item => `
                        <li>${item.product.name} (x${item.quantity}) - $${item.subtotal.toFixed(2)}</li>
                    `).join('')}
                </ul>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load orders:', error);
    }
}
            </div>
        `;
    }).join('');
    
    totalEl.innerText = `$${total.toFixed(2)}`;
}

// Checkout Logic
async function checkout() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert("Please login first!");
        return;
    }

    const orderData = {
        items: cart.map(item => ({ product_id: item.id, quantity: item.quantity }))
    };

    const response = await fetch(`${API_URL}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(orderData)
    });

    if (response.ok) {
        alert("Order placed successfully!");
        cart = [];
        updateCartUI();
    } else {
        alert("Failed to place order.");
    }
}

// --- Wishlist Functionality ---
async function addToWishlist(productId, userId) {
    const response = await fetch(`/api/wishlist?user_id=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
    });

    if (response.ok) {
        alert("Added to wishlist!");
    } else {
        alert("Failed to add to wishlist.");
    }
}

// --- Coupon Functionality ---
async function applyCoupon(code) {
    const response = await fetch('/api/coupons/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code })
    });

    const data = await response.json();
    if (response.ok) {
        alert(`Coupon applied! You get ${data.discount_percent}% off.`);
        // Logic to update total price would go here
    } else {
        alert(data.detail || "Invalid coupon");
    }
}