base_url = "http://0.0.0.0:8080"
import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDMwOTU3MTAsIm5iZiI6MTYwMzA5NTcxMCwianRpIjoiZTZhNDIwYzItNjJjYS00MTUyLTlmNWYtZTUxMjQwZGZlZjU2IiwiZXhwIjoxNjAzMDk2NjEwLCJpZGVudGl0eSI6Im5oZDM2IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.6klVBQBtOLGQLKUJLCXx68gGTXXqHGGDl4CH3ppJAPQ"
def document_api(document_name, token, method, new_name="None", content="None"):
    url = f"{base_url}/document/{document_name}"
    if method == "GET":
        headers = {"Authorization": token}
        result = requests.get(url, headers=headers).json()
    elif method == "POST":
        headers = {"Authorization": token}
        data = {"content": "Hello"}
        result = requests.post(url, headers=headers, data=data).json()
    elif method == "PUT":
        headers = {"Authorization": token}
        result = requests.put(url, headers=headers).json()
    elif method == "DELETE":
        headers = {"Authorization": token}
        result = requests.delete(url, headers=headers).json()
    return result

result = document_api("Nam", token, "POST", "Nam", "Nam")
print(result)
