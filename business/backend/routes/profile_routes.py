from flask import Blueprint, request, session
from backend.database import query_db
from backend.utils.helpers import login_required, api_response

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    """Fetches user personal, business, financial details and goals."""
    user_id = session.get('user_id')
    user = query_db("SELECT full_name, mobile, email FROM users WHERE id = ?", (user_id,), one=True)
    ent = query_db("SELECT * FROM entrepreneurs WHERE user_id = ?", (user_id,), one=True)
    b_profile = query_db("SELECT * FROM business_profiles WHERE user_id = ?", (user_id,), one=True)

    data = {
        "user": user or {},
        "entrepreneur": ent or {},
        "business_profile": b_profile or {}
    }
    return api_response(success=True, data=data)

@profile_bp.route('/api/profile', methods=['PUT', 'POST'])
@login_required
def update_profile():
    """Updates entrepreneur profile, financial details, goals, and onboarding status."""
    user_id = session.get('user_id')
    data = request.get_json() or {}

    # Fields
    full_name = data.get('name') or data.get('full_name')
    village_town = data.get('village_town')
    district = data.get('district')
    state = data.get('state')
    business_type = data.get('business_type')
    business_status = data.get('business_status', 'Operational')
    years_in_business = float(data.get('years_in_business') or 0)
    number_of_workers = int(data.get('number_of_workers') or 1)
    initial_investment = float(data.get('initial_investment') or 0)
    monthly_revenue = float(data.get('monthly_revenue') or 0)
    monthly_expenses = float(data.get('monthly_expenses') or 0)
    current_savings = float(data.get('current_savings') or 0)
    existing_loan = float(data.get('existing_loan') or 0)
    goals = data.get('goals')
    if isinstance(goals, list):
        goals = ", ".join(goals)

    if full_name:
        query_db("UPDATE users SET full_name = ? WHERE id = ?", (full_name, user_id), commit=True)
        session['user_name'] = full_name

    # Check if entrepreneur record exists
    ent = query_db("SELECT id FROM entrepreneurs WHERE user_id = ?", (user_id,), one=True)
    if ent:
        query_db(
            """UPDATE entrepreneurs SET
               village_town = ?, district = ?, state = ?, business_type = ?,
               business_status = ?, years_in_business = ?, number_of_workers = ?,
               initial_investment = ?, monthly_revenue = ?, monthly_expenses = ?,
               current_savings = ?, existing_loan = ?, goals = ?, is_onboarded = 1
               WHERE user_id = ?""",
            (village_town, district, state, business_type, business_status,
             years_in_business, number_of_workers, initial_investment,
             monthly_revenue, monthly_expenses, current_savings, existing_loan,
             goals, user_id),
            commit=True
        )
    else:
        query_db(
            """INSERT INTO entrepreneurs
               (user_id, village_town, district, state, business_type, business_status,
                years_in_business, number_of_workers, initial_investment, monthly_revenue,
                monthly_expenses, current_savings, existing_loan, goals, is_onboarded)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
            (user_id, village_town, district, state, business_type, business_status,
             years_in_business, number_of_workers, initial_investment, monthly_revenue,
             monthly_expenses, current_savings, existing_loan, goals),
            commit=True
        )

    # Update business details if provided
    b_name = data.get('business_name')
    if b_name:
        b_cat = data.get('business_category', business_type)
        t_cust = data.get('target_customers', 'Local village households')
        prod = data.get('products_services', business_type)
        exp_sales = float(data.get('expected_monthly_sales') or monthly_revenue)
        
        b_prof = query_db("SELECT id FROM business_profiles WHERE user_id = ?", (user_id,), one=True)
        if b_prof:
            query_db(
                """UPDATE business_profiles SET business_name = ?, business_category = ?,
                   target_customers = ?, products_services = ?, expected_monthly_sales = ?
                   WHERE user_id = ?""",
                (b_name, b_cat, t_cust, prod, exp_sales, user_id),
                commit=True
            )
        else:
            query_db(
                """INSERT INTO business_profiles (user_id, business_name, business_category, target_customers, products_services, expected_monthly_sales)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, b_name, b_cat, t_cust, prod, exp_sales),
                commit=True
            )

    return api_response(success=True, message="Profile and business information updated successfully!")
