import jwt
import requests
import socket
from config import API_KEY, API_SECRET, ALLOWED_PROFILE_EXTENSIONS

def scan_OCR(file):

    url = 'https://demo.computervision.com.vn/backend/api/v1/request/text_photostory/get_scan_a4'
    response = requests.post(url, auth=(API_KEY, API_SECRET), files={'image':file})
    if response.status_code != 200:
        return 1, "Cannot scan image"
    result = response.json()["result"]
    content = ""
    for line in result:
        content += line + "\n"
    return 0, content

def allowed_file(filename):
    file_type = filename.split(".")[1]
    if file_type in ALLOWED_PROFILE_EXTENSIONS:
        return True
    return False


def decode_user(jwt_token):
    decoded_jwt = jwt.decode(jwt_token, 'super-secret', algorithm='HS256')
    username = decoded_jwt['identity']
    return username
