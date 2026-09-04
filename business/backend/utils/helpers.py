from flask import jsonify, session, request
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Secure password hashing using PBKDF2/scrypt via Werkzeug."""
    return generate_password_hash(password, method='scrypt')

def verify_password(password_hash, password):
    """Verifies a plain password against the stored hash."""
    return check_password_hash(password_hash, password)

def api_response(success=True, message="", data=None, status_code=200):
    """Standardized API JSON response helper."""
    response = {
        "success": success,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(response), status_code

def login_required(f):
    """Decorator to enforce session authentication for protected API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return api_response(success=False, message="Unauthorized. Please log in first.", status_code=401)
        return f(*args, **kwargs)
    return decorated_function

def format_currency_inr(amount):
    """Formats numbers into standard Indian Rupee notation (e.g. ₹1,00,000)."""
    try:
        val = float(amount)
        s = f"{val:,.2f}"
        return f"₹{s}"
    except (ValueError, TypeError):
        return "₹0.00"
