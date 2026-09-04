from flask import Blueprint, request, session
from backend.database import query_db
from backend.utils.helpers import hash_password, verify_password, api_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """Handles user registration, creates user and entrepreneur profile record."""
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    mobile = data.get('mobile', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    village_town = data.get('village_town', '').strip()
    district = data.get('district', '').strip()
    state = data.get('state', '').strip()
    business_type = data.get('business_type', '').strip()

    if not full_name or not mobile or not email or not password:
        return api_response(success=False, message="All required fields (Name, Mobile, Email, Password) must be provided.", status_code=400)

    # Check existing email or mobile
    existing_user = query_db("SELECT id FROM users WHERE email = ? OR mobile = ?", (email, mobile), one=True)
    if existing_user:
        return api_response(success=False, message="A user with this Email or Mobile number already exists.", status_code=409)

    pwd_hash = hash_password(password)
    
    try:
        user_id = query_db(
            "INSERT INTO users (full_name, mobile, email, password_hash) VALUES (?, ?, ?, ?)",
            (full_name, mobile, email, pwd_hash),
            commit=True
        )

        # Create initial entrepreneur profile
        query_db(
            """INSERT INTO entrepreneurs 
               (user_id, village_town, district, state, business_type, is_onboarded) 
               VALUES (?, ?, ?, ?, ?, 0)""",
            (user_id, village_town, district, state, business_type),
            commit=True
        )

        # Set session
        session['user_id'] = user_id
        session['user_name'] = full_name
        session['user_email'] = email

        return api_response(
            success=True,
            message="Registration successful! Welcome to GramBiz AI.",
            data={"user_id": user_id, "full_name": full_name, "is_onboarded": False},
            status_code=201
        )
    except Exception as e:
        return api_response(success=False, message=f"Registration failed: {str(e)}", status_code=500)

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Handles user authentication."""
    data = request.get_json() or {}
    identifier = data.get('email_or_mobile', '').strip().lower()
    password = data.get('password', '')

    if not identifier or not password:
        return api_response(success=False, message="Please enter both identifier (email/mobile) and password.", status_code=400)

    user = query_db(
        "SELECT id, full_name, email, password_hash FROM users WHERE email = ? OR mobile = ?",
        (identifier, identifier),
        one=True
    )

    if not user or not verify_password(user['password_hash'], password):
        return api_response(success=False, message="Invalid email/mobile or password.", status_code=401)

    # Fetch onboarding status
    ent = query_db("SELECT is_onboarded FROM entrepreneurs WHERE user_id = ?", (user['id'],), one=True)
    is_onboarded = bool(ent['is_onboarded']) if ent else False

    session['user_id'] = user['id']
    session['user_name'] = user['full_name']
    session['user_email'] = user['email']

    return api_response(
        success=True,
        message="Login successful!",
        data={
            "user_id": user['id'],
            "full_name": user['full_name'],
            "email": user['email'],
            "is_onboarded": is_onboarded
        }
    )

@auth_bp.route('/api/logout', methods=['POST', 'GET'])
def logout():
    """Clears user session."""
    session.clear()
    return api_response(success=True, message="Logged out successfully.")

@auth_bp.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Returns current active session status."""
    user_id = session.get('user_id')
    if not user_id:
        return api_response(success=False, message="Not authenticated", data={"is_authenticated": False})
    
    user = query_db("SELECT id, full_name, email FROM users WHERE id = ?", (user_id,), one=True)
    ent = query_db("SELECT is_onboarded, village_town, district, state, business_type FROM entrepreneurs WHERE user_id = ?", (user_id,), one=True)
    
    return api_response(
        success=True,
        message="Authenticated",
        data={
            "is_authenticated": True,
            "user_id": user_id,
            "full_name": user['full_name'] if user else session.get('user_name'),
            "email": user['email'] if user else session.get('user_email'),
            "is_onboarded": bool(ent['is_onboarded']) if ent else False,
            "profile": ent if ent else {}
        }
    )
