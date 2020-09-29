import requests

api_key = 'e37bafa70cd7411bb5be4df45cdbcc4e'
api_secret = '4b4074d73e0b8efc2870d958c2faf8aa8bdcbae63cff2b5706ed1247bf576cd3'
url = 'https://demo.computervision.com.vn/backend/api/v1/request/text_photostory/get_scan_a4'
image_path = 'C:\\Users\\daoha\\Documents\\Projects\\PythonProject\\ComputerVisionVietnam\\Backend_OCR_Document\\TestImage\\essay.jpg'

nam = open(image_path, 'rb')
print(type(nam))
# response = requests.post(url, auth=(api_key, api_secret), files={'image': open(image_path, 'rb')}).json()
#
# result = response['result']
#
# content = ""
#
# for line in result:
#     content += line + " "
#
# print(content)
