import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'grambiz_default_secret_key_2026')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    
    USE_MYSQL = os.getenv('USE_MYSQL', 'false').lower() == 'true'
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'grambiz_db')
    
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLITE_DB_PATH = os.path.join(BASE_DIR, 'database', 'grambiz.db')
