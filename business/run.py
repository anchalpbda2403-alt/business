import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.config import Config

app = create_app()

if __name__ == '__main__':
    print("=" * 65)
    print(" GramBiz AI - Hyperlocal Rural Business & Financial Assistant")
    print(f" Running locally on: http://127.0.0.1:{Config.PORT}")
    print("=" * 65)
    app.run(host='127.0.0.1', port=Config.PORT, debug=True)
