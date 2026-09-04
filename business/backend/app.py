import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from backend.config import Config
from backend.database import init_sqlite_db

# Import Blueprints
from backend.routes.auth_routes import auth_bp
from backend.routes.profile_routes import profile_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.finance_routes import finance_bp
from backend.routes.advisor_routes import advisor_bp
from backend.routes.notification_routes import notification_bp

def create_app():
    # Setup template/static folder pointing to frontend
    frontend_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    app = Flask(__name__, static_folder=frontend_folder, static_url_path='')
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, supports_credentials=True)

    # Initialize SQLite database if fallback is active
    init_sqlite_db()

    # Register API Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(advisor_bp)
    app.register_blueprint(notification_bp)

    # Serve static HTML pages
    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_folder, 'index.html')

    @app.route('/<path:filename>')
    def serve_static_file(filename):
        if os.path.exists(os.path.join(frontend_folder, filename)):
            return send_from_directory(frontend_folder, filename)
        # SPA or fall back to index.html
        return send_from_directory(frontend_folder, 'index.html')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
