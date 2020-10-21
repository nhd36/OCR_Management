from dotenv import load_dotenv
import os

load_dotenv()

APP_PORT = os.getenv("APP_PORT")
API_PORT = os.getenv("API_PORT")
IP = os.getenv("IP")

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

ALLOWED_PROFILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
