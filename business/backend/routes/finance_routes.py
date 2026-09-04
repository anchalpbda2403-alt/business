from flask import Blueprint, request, session
from backend.database import query_db
from backend.services.financial_engine import FinancialEngine
from backend.utils.helpers import login_required, api_response

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/api/financial-analysis', methods=['POST'])
@login_required
def financial_analysis():
    """Calculates financial metrics (Break-even, EMI, Margins, Projections, Funding Gap)."""
    data = request.get_json() or {}
    results = FinancialEngine.perform_financial_structuring(data)
    return api_response(success=True, data=results)

@finance_bp.route('/api/expenses', methods=['GET'])
@login_required
def get_expenses():
    """Fetches user expenses list, total sum, category breakdown, and monthly chart data."""
    user_id = session.get('user_id')
    expense_list = query_db(
        "SELECT id, expense_date, category, description, amount FROM expenses WHERE user_id = ? ORDER BY expense_date DESC",
        (user_id,)
    )

    total_exp = sum(float(x['amount']) for x in expense_list)
    
    # Category totals
    cat_totals = {}
    for x in expense_list:
        cat = x['category']
        cat_totals[cat] = cat_totals.get(cat, 0.0) + float(x['amount'])

    return api_response(
        success=True,
        data={
            "expenses": expense_list,
            "total_expenses": total_exp,
            "category_totals": cat_totals
        }
    )

@finance_bp.route('/api/expenses', methods=['POST'])
@login_required
def add_expense():
    """Logs a new expense transaction."""
    user_id = session.get('user_id')
    data = request.get_json() or {}
    exp_date = data.get('date')
    category = data.get('category')
    description = data.get('description', '')
    amount = float(data.get('amount') or 0)

    if not exp_date or not category or amount <= 0:
        return api_response(success=False, message="Date, Category, and valid Amount are required.", status_code=400)

    exp_id = query_db(
        "INSERT INTO expenses (user_id, expense_date, category, description, amount) VALUES (?, ?, ?, ?, ?)",
        (user_id, exp_date, category, description, amount),
        commit=True
    )

    return api_response(success=True, message="Expense added successfully!", data={"id": exp_id})

@finance_bp.route('/api/revenue', methods=['GET'])
@login_required
def get_revenue():
    """Fetches user revenue sales list, daily total, monthly total, and best-selling product."""
    user_id = session.get('user_id')
    rev_list = query_db(
        "SELECT id, revenue_date, product_service, quantity, amount FROM revenues WHERE user_id = ? ORDER BY revenue_date DESC",
        (user_id,)
    )

    total_rev = sum(float(x['amount']) for x in rev_list)

    # Product sales aggregation
    prod_sales = {}
    for x in rev_list:
        p = x['product_service']
        prod_sales[p] = prod_sales.get(p, 0.0) + float(x['amount'])

    best_selling = max(prod_sales.items(), key=lambda x: x[1])[0] if prod_sales else "N/A"

    return api_response(
        success=True,
        data={
            "revenues": rev_list,
            "total_revenue": total_rev,
            "best_selling_product": best_selling,
            "product_breakdown": prod_sales
        }
    )

@finance_bp.route('/api/revenue', methods=['POST'])
@login_required
def add_revenue():
    """Logs a new revenue sales transaction."""
    user_id = session.get('user_id')
    data = request.get_json() or {}
    rev_date = data.get('date')
    product = data.get('product_service')
    quantity = int(data.get('quantity') or 1)
    amount = float(data.get('amount') or 0)

    if not rev_date or not product or amount <= 0:
        return api_response(success=False, message="Date, Product/Service, and valid Amount are required.", status_code=400)

    rev_id = query_db(
        "INSERT INTO revenues (user_id, revenue_date, product_service, quantity, amount) VALUES (?, ?, ?, ?, ?)",
        (user_id, rev_date, product, quantity, amount),
        commit=True
    )

    return api_response(success=True, message="Revenue record logged successfully!", data={"id": rev_id})
