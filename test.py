import requests

def scan_OCR(file):

    url = 'https://demo.computervision.com.vn/backend/api/v1/request/text_photostory/get_scan_a4'
    response = requests.post(url, auth=(API_KEY, API_SECRET), files={'image':file}).json()
    print(response.status_code)
    content = ""
    # for line in result:
    #     content += line + " "
    #
    return 0, content

scan_OCR()
