from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_PROFILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
API_PORT = os.getenv("API_PORT")
IP = os.getenv("IP")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Messages Deny (Status = 1):
MESSAGE_NO_TOKEN_HEADER = {"status": 1, "message": "Please included Token Headers"}
MESSAGE_LOGGED_OUT = {"status": 1, "message": "You already logged out. Please log back in"}
MESSAGE_DOC_NOT_FOUND = {"status": 1, "message": "Document does not exist."}
MESSAGE_DOC_EXIST = {"status": 1, "message": "Document name has already existed. Please pick another name"}
MESSAGE_USER_EXIST = {"status": 1, "message": "Username has already existed, please try another one."}
MESSAGE_TOKEN_EXPIRED = {"status": 1, "message": "Your token has expired, please log in again!"}
MESSAGE_UNEXPECTED_ERROR = {"status": 1, "message": "Internal Error, please log back in"}
MESSAGE_UNREADABLE = {"status": 1, "message": "Cannot read image, please try another one!"}

# Messages Accept (Status = 0):
MESSAGE_DOC_CREATED_SUCCESS = {"status": 0, "message": "Document successfully saved to Database!"}
MESSAGE_DOC_DELETED_SUCCESS = {"status": 0, "message": "Successfully delete document!"}
MESSAGE_USER_REGISTER_SUCCESS = {"status": 0, "message": "User registered successfully!"}
MESSAGE_USER_LOGOUT_SUCCESS = {"status": 0, "message": "LogOut Successfully"}

# Status Code:
SC_UNAUTHORIZED = 401
SC_RESET_CONTENT = 205
SC_SUCCESS = 200
SC_NOT_FOUND = 404
SC_BAD_REQUEST = 400
SC_CREATE = 201
SC_CONFLICT = 409
SC_UNEXPECTED_ERR = 500
