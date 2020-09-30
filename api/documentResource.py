from flask_restful import Resource, reqparse
import werkzeug
from io import BufferedReader
from side_methods import scan_OCR, allowed_file
from models.userModel import UserModel
from models.documentModel import DocumentModel

class Document(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help='Please input your password')

    def get(self, username, doc_name):
        data = self.parser.parse_args()
        password = data["password"]
        if not UserModel.account_credential(username, password):
            return {"message": "Invalid account, please try again."}, 401
        docs = DocumentModel.find_doc_by_name(username, doc_name)
        if docs:
            return {"message": "success",
                    "documents": docs}, 200
        return {"message": "Document does not exist."}, 404


    def post(self, username, doc_name):
        self.parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True, help="No header 'file' found")
        data = self.parser.parse_args()
        file = data['file']
        password = data['password']
        if not UserModel.account_credential(username, password):
            return {"message": "Invalid account, please try again."}, 401
        if data['file'].filename == '':
            return {"message": "No file found. Please input file"}, 400
        if not allowed_file(file.filename):
            return {"message": "File type not support. Please input the following type: PNG, JPG, JPEG"}, 400

        image_file = BufferedReader(file)
        result_scan = scan_OCR(image_file)
        user_id = UserModel.find_user_by_username(username).id
        doc = DocumentModel(user_id, doc_name, result_scan)
        doc.save_to_db()

        return {"message": "Document successfully saved to Database!"}, 201


    def delete(self, username, doc_name):
        self.parser.add_argument('doc_id', type=int, required=True, help='Please input document ID')
        data = self.parser.parse_args()
        doc_id = data['doc_id']
        password = data['password']
        if not UserModel.account_credential(username, password):
            return {"message": "Invalid account, please try again."}, 401
        doc = DocumentModel.find_doc_by_id(username, doc_id)
        if doc:
            DocumentModel.delete_doc(username, doc_name, doc_id)
            return {"message": "Successfully delete document!"}
        return {"message": "Document doesn't exist"}

class Documents(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help='Please input your password')

    def get(self, username):
        data = self.parser.parse_args()
        password = data['password']
        if not UserModel.account_credential(username, password):
            return {"message": "Invalid account, please try again."}, 401

        docs = DocumentModel.get_all_user_docs(username)
        return {"message": "success",
                "documents": docs}, 200
