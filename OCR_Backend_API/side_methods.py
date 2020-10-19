import requests
import socket
from config import API_KEY, API_SECRET, ALLOWED_PROFILE_EXTENSIONS

def scan_OCR(file):

    url = 'https://demo.computervision.com.vn/backend/api/v1/request/text_photostory/get_scan_a4'
    response = requests.post(url, auth=(API_KEY, API_SECRET), files={'image':file}).json()
    result = response['result']
    content = ""
    for line in result:
        content += line + " "

    return content

def allowed_file(filename):
    file_type = filename.split(".")[1]
    if file_type in ALLOWED_PROFILE_EXTENSIONS:
        return True
    return False

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
