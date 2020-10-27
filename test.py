import requests

def register_api(first_name, last_name, username, password):
    url = "http://0.0.0.0:8080/register"
    data = {"first_name": first_name, "last_name": last_name, "username": username, "password": password}
    result = requests.post(url, data=data).json()
    return result

nam = register_api("Nam", "Dao", "nhd37", "inthoi");
print(nam)
