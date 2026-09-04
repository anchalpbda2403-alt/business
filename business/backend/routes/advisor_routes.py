from flask import Blueprint, request, session
from backend.database import query_db
from backend.services.ai_service import AIService
from backend.services.hyperlocal_service import HyperlocalService
from backend.utils.helpers import login_required, api_response

advisor_bp = Blueprint('advisor', __name__)

@advisor_bp.route('/api/business-advice', methods=['POST'])
@login_required
def get_business_advice():
    """AI Advisor Chatbot API endpoint."""
    user_id = session.get('user_id')
    data = request.get_json() or {}
    message = data.get('message', '').strip()

    if not message:
        return api_response(success=False, message="Message cannot be empty.", status_code=400)

    # Save user message to database
    query_db("INSERT INTO chat_history (user_id, sender, message) VALUES (?, 'user', ?)", (user_id, message), commit=True)

    # Get profile context
    user = query_db("SELECT full_name FROM users WHERE id = ?", (user_id,), one=True)
    ent = query_db("SELECT * FROM entrepreneurs WHERE user_id = ?", (user_id,), one=True)
    
    profile_ctx = {
        "name": user['full_name'] if user else "Entrepreneur",
        "village_town": ent.get('village_town', '') if ent else "",
        "district": ent.get('district', '') if ent else "",
        "state": ent.get('state', '') if ent else "",
        "business_type": ent.get('business_type', '') if ent else "",
        "monthly_revenue": ent.get('monthly_revenue', 0) if ent else 0,
        "monthly_expenses": ent.get('monthly_expenses', 0) if ent else 0,
        "current_savings": ent.get('current_savings', 0) if ent else 0,
        "initial_investment": ent.get('initial_investment', 0) if ent else 0
    }

    # Generate response
    reply_text = AIService.generate_chat_reply(message, profile_ctx)

    # Save assistant response to database
    query_db("INSERT INTO chat_history (user_id, sender, message) VALUES (?, 'assistant', ?)", (user_id, reply_text), commit=True)

    return api_response(success=True, data={"reply": reply_text})

@advisor_bp.route('/api/chat-history', methods=['GET'])
@login_required
def get_chat_history():
    """Retrieves chat message history for the user."""
    user_id = session.get('user_id')
    history = query_db("SELECT sender, message, created_at FROM chat_history WHERE user_id = ? ORDER BY id ASC", (user_id,))
    return api_response(success=True, data={"history": history})

@advisor_bp.route('/api/business-plan', methods=['POST'])
@login_required
def generate_plan():
    """Generates structured 11-section business plan."""
    data = request.get_json() or {}
    plan = AIService.generate_business_plan(data)
    return api_response(success=True, data={"business_plan": plan})

@advisor_bp.route('/api/hyperlocal-insights', methods=['GET', 'POST'])
@login_required
def hyperlocal_insights():
    """Returns local business opportunities and area analysis."""
    user_id = session.get('user_id')
    ent = query_db("SELECT village_town, district, state, initial_investment FROM entrepreneurs WHERE user_id = ?", (user_id,), one=True)
    
    district = ent.get('district', 'Your Area') if ent else 'Your Area'
    budget = ent.get('initial_investment', 50000) if ent else 50000

    opportunities = HyperlocalService.get_opportunities(location=district, budget=budget)
    area_report = HyperlocalService.analyze_area(
        ent.get('village_town', '') if ent else '',
        district,
        ent.get('state', '') if ent else ''
    )

    return api_response(success=True, data={
        "opportunities": opportunities,
        "area_report": area_report,
        "user_location": f"{ent.get('village_town', '')}, {district}, {ent.get('state', '')}" if ent else "Rural Area"
    })
