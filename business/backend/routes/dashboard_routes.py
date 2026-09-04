from flask import Blueprint, session
from backend.database import query_db
from backend.services.financial_engine import FinancialEngine
from backend.utils.helpers import login_required, api_response

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    """Returns aggregated KPIs, health score, charts, and recommendations for dashboard."""
    user_id = session.get('user_id')
    user = query_db("SELECT full_name FROM users WHERE id = ?", (user_id,), one=True)
    ent = query_db("SELECT * FROM entrepreneurs WHERE user_id = ?", (user_id,), one=True)
    
    # Calculate sum of expenses & revenues from table logs if logged
    exp_sum = query_db("SELECT SUM(amount) as total FROM expenses WHERE user_id = ?", (user_id,), one=True)
    rev_sum = query_db("SELECT SUM(amount) as total FROM revenues WHERE user_id = ?", (user_id,), one=True)

    logged_expenses = float(exp_sum['total'] or 0) if exp_sum and exp_sum['total'] else 0
    logged_revenue = float(rev_sum['total'] or 0) if rev_sum and rev_sum['total'] else 0

    monthly_revenue = logged_revenue if logged_revenue > 0 else float(ent.get('monthly_revenue', 40000) if ent else 40000)
    monthly_expenses = logged_expenses if logged_expenses > 0 else float(ent.get('monthly_expenses', 25000) if ent else 25000)
    current_savings = float(ent.get('current_savings', 15000) if ent else 15000)
    existing_loan = float(ent.get('existing_loan', 0) if ent else 0)
    initial_inv = float(ent.get('initial_investment', 100000) if ent else 100000)

    estimated_profit = monthly_revenue - monthly_expenses
    available_cash = current_savings
    funding_req = max(0, initial_inv - (current_savings + existing_loan))

    # Health score evaluation
    health_eval = FinancialEngine.calculate_health_score(
        monthly_revenue, monthly_expenses, current_savings, existing_loan
    )

    # Dynamic recommendations
    recommendations = []
    if monthly_expenses > (monthly_revenue * 0.70):
        recommendations.append("Your expenses exceed 70% of revenue this month. Consider reducing bulk transport and raw material costs.")
    else:
        recommendations.append("Expenses are well maintained. Reinvest part of surplus revenue into inventory.")

    if estimated_profit > 10000:
        recommendations.append("Direct customer sales in nearby Haats can boost your monthly profit margins further.")
    
    if available_cash < monthly_expenses:
        recommendations.append("Maintain an emergency cash reserve of at least 3 months operating expenses.")
    else:
        recommendations.append("You have established a good cash buffer for quiet operational months.")

    # Generate Chart Data
    months_labels = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    rev_chart = [round(monthly_revenue * 0.85), round(monthly_revenue * 0.90), round(monthly_revenue * 0.95), round(monthly_revenue * 0.98), round(monthly_revenue * 1.02), round(monthly_revenue)]
    exp_chart = [round(monthly_expenses * 0.90), round(monthly_expenses * 0.92), round(monthly_expenses * 0.95), round(monthly_expenses * 0.96), round(monthly_expenses * 0.98), round(monthly_expenses)]
    profit_chart = [r - e for r, e in zip(rev_chart, exp_chart)]

    data = {
        "user_name": user['full_name'] if user else "Entrepreneur",
        "business_type": ent.get('business_type', 'Micro Business') if ent else "Micro Business",
        "location": f"{ent.get('village_town', '')}, {ent.get('district', '')}" if ent else "",
        "kpis": {
            "health_score": health_eval['score'],
            "health_rating": health_eval['rating'],
            "monthly_revenue": monthly_revenue,
            "monthly_expenses": monthly_expenses,
            "estimated_profit": estimated_profit,
            "available_cash": available_cash,
            "funding_requirement": funding_req
        },
        "health_eval": health_eval,
        "recommendations": recommendations,
        "chart_data": {
            "labels": months_labels,
            "revenue": rev_chart,
            "expenses": exp_chart,
            "profit": profit_chart
        }
    }

    return api_response(success=True, data=data)
