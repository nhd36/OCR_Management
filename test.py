base_url = "http://0.0.0.0:8080"
import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDMyNjYxODgsIm5iZiI6MTYwMzI2NjE4OCwianRpIjoiNzQ5ZjVhY2MtMDAyOS00MjIyLWIxNzMtNDVmMWU1ZDQwNmVmIiwiZXhwIjoxNjAzMjY3MDg4LCJpZGVudGl0eSI6Im5oZDM2IiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.DEuvhkIFQPJ8IJk0feTud6-qjkVXFDfEV1k9BD3Rmhw"

def reader_api(token, image_file):
    url = f"{base_url}/reader"
    headers = {"Authorization": token}
    data = {"file": image_file}
    result = requests.post(url, headers=headers, data=data).json()
    return result

result = reader_api(token, "essay.jpg")
print(result)
