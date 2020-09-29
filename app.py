from flask import Flask
from flask_restful import Api, Resource, reqparse
import werkzeug
import requests
from io import BufferedReader
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Model/doc_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    document = db.relationship('DocumentModel', back_populates='user')

    def __init__(self, _id, first_name, last_name, email, password):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.id}_{self.first_name}_{self.last_name}_{self.email}_{self.password}"

class DocumentModel(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doc_name = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('UserModel', back_populates='document')

    def __init__(self, _id, user_id, doc_name, content):
        self.id = user_id
        self.__user_id = user_id
        self.__doc_name = doc_name
        self.__content = content


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

class Document(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True, help="No header 'file' found")

    def get(self, doc_name):
        data = self.parse.parse_args()
        return doc_name, 201

    def post(self, doc_name):
        data = self.parser.parse_args()
        file = data['file']
        if data['file'].filename == '':
            return {"message": "No file found. Please input file"}
        if not allowed_file(file.filename):
            return {"message": "File type not support. Please input the following type: PNG, JPG, JPEG"}

        image_file = BufferedReader(file)
        result_scan = scan_OCR(image_file)

        return {"doc_name": doc_name, "content": result_scan}

api.add_resource(Document, "/<string:doc_name>")
if __name__ == '__main__':
    app.run(debug=True)
