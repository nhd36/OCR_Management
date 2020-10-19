from app import app
from config import APP_PORT, IP

if __name__ == '__main__':
    app.run(debug=True, host=IP, port=APP_PORT)
