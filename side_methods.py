import requests
import socket

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def scan_OCR(file):

    api_key = 'e37bafa70cd7411bb5be4df45cdbcc4e'
    api_secret = '4b4074d73e0b8efc2870d958c2faf8aa8bdcbae63cff2b5706ed1247bf576cd3'
    url = 'https://demo.computervision.com.vn/backend/api/v1/request/text_photostory/get_scan_a4'
    response = requests.post(url, auth=(api_key, api_secret), files={'image':file}).json()
    result = response['result']
    content = ""
    for line in result:
        content += line + " "

    return content

def allowed_file(filename):
    file_type = filename.split(".")[1]
    if file_type in ALLOWED_EXTENSIONS:
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
