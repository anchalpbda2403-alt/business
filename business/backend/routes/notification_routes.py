from flask import Blueprint, session
from backend.database import query_db
from backend.utils.helpers import login_required, api_response

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    """Retrieves user notifications and alerts."""
    user_id = session.get('user_id')
    user_notifs = query_db("SELECT id, title, message, type, is_read, created_at FROM notifications WHERE user_id = ? ORDER BY id DESC", (user_id,))
    
    # Default smart alerts if none recorded in DB
    if not user_notifs:
        user_notifs = [
            {
                "id": 1,
                "title": "Expense Tracking Alert",
                "message": "Your monthly expenses increased by 12% compared to last month.",
                "type": "warning",
                "is_read": 0,
                "created_at": "Today"
            },
            {
                "id": 2,
                "title": "Sales Performance",
                "message": "Your revenue improved this month! Keep tracking daily sales.",
                "type": "success",
                "is_read": 0,
                "created_at": "Yesterday"
            },
            {
                "id": 3,
                "title": "Cash Flow Tip",
                "message": "Review your cash flow and build a 3-month operational buffer.",
                "type": "info",
                "is_read": 1,
                "created_at": "3 days ago"
            },
            {
                "id": 4,
                "title": "Profile Update",
                "message": "Update your business information to unlock custom AI advice.",
                "type": "info",
                "is_read": 1,
                "created_at": "1 week ago"
            }
        ]

    return api_response(success=True, data={"notifications": user_notifs, "unread_count": len([n for n in user_notifs if not n.get('is_read')])})
