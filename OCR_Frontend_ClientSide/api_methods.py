import requests
from config import API_PORT, IP

base_url = f"http://{IP}:{API_PORT}"

def login_api(username, password):
    url = f"{base_url}/login"
    data = {"username": username, "password": password}
    result = requests.post(url, data=data).json()
    return result

def register_api(first_name, last_name, username, password):
    url = f"{base_url}/register"
    data = {"first_name": first_name, "last_name": last_name, "username": username, "password": password}
    result = requests.post(url, data=data).json()
    return result

def document_api(document_name, token, method, content="None", new_name="None"):
    url = f"{base_url}/document/{document_name}"
    if method == "GET":
        headers = {"Authorization": token}
        result = requests.get(url, headers=headers).json()
    elif method == "POST":
        headers = {"Authorization": token}
        data = {"content": content}
        result = requests.post(url, headers=headers, data=data).json()
    elif method == "PUT":
        headers = {"Authorization": token}
        data = {"new_name": new_name, "content": content}
        result = requests.put(url, headers=headers, data=data).json()
    elif method == "DELETE":
        headers = {"Authorization": token}
        result = requests.delete(url, headers=headers).json()
    return result

def documents_api(token):
    url = f"{base_url}/documents"
    headers = {"Authorization": token}
    result = requests.get(url, headers=headers).json()
    return result

def logout_api(token):
    url = f"{base_url}/logout"
    headers = {"Authorization": token}
    result = requests.get(url, headers=headers).json()
    return result

def searchkeywords_api(token, keywords):
    url = f"{base_url}/searchkeywords"
    headers = {"Authorization": token}
    data = {"keywords": keywords}
    result = requests.post(url, headers=headers, data=data).json()
    return result

def reader_api(token, image_file):
    url = f"{base_url}/reader"
    headers = {"Authorization": token}
    result = requests.post(url, headers=headers, data=image_file).json()
    return result

def validateUser_api(token):
    url = f"{base_url}/authorize_user"
    headers = {"Authorization": token}
    result = requests.get(url, headers=headers).json()
    return result
