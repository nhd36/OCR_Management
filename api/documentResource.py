from flask import request
from flask_restful import Resource, reqparse
import werkzeug
from io import BufferedReader
from side_methods import scan_OCR, allowed_file
from models.userModel import UserModel
from models.documentModel import DocumentModel
from models.tokenModel import TokenModel
import jwt

class Document(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('doc_id', type=int, help='Document ID must be integer')
    parser.add_argument('new_name', type=str, help='Document name must be String')
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')

    def get(self, doc_name):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}
        username = UserModel.decode_user(access_token)
        docs = DocumentModel.find_doc_by_name(username, doc_name)
        if docs:
            return {"message": "success",
                    "username": username,
                    "documents": docs}, 200
        return {"message": "Document does not exist."}, 404


    def post(self, doc_name):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}

        username = UserModel.decode_user(access_token)

        self.parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True, help="No header 'file' found")
        data = self.parser.parse_args()
        file = data['file']

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


    def delete(self, doc_name):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}

        username = UserModel.decode_user(access_token)

        data = self.parser.parse_args()
        if "doc_id" not in data:
            return {"message": "Please input document ID"}
        doc_id = data['doc_id']
        doc = DocumentModel.find_doc_by_id(username, doc_id)
        if doc:
            DocumentModel.delete_doc(username, doc_name, doc_id)
            return {"message": "Successfully delete document!"}
        return {"message": "Document doesn't exist"}

    def put(self, doc_name):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}

        username = UserModel.decode_user(access_token)

        data = self.parser.parse_args()
        if "doc_id" not in data:
            return {"message": "Please input document ID"}
        if "new_name" not in data:
            return {"message": "Please input new name for the document"}

        doc_id = data['doc_id']
        file = data['file']
        new_name = data['new_name']

        if data['file'].filename == '':
            return {"message": "No file found. Please input file"}, 400
        if not allowed_file(file.filename):
            return {"message": "File type not support. Please input the following type: PNG, JPG, JPEG"}, 400

        image_file = BufferedReader(file)
        try:
            result_scan = scan_OCR(image_file)
        except:
            return {"message": "Cannot read input file. Please try another file"}

        doc = DocumentModel.find_doc_by_id(username, doc_id)
        if doc:
            DocumentModel.update_doc_by_id(username, doc_id, result_scan, new_name)
            return {"message": "Successfully update document!"}

        user_id = UserModel.find_user_by_username(username).id
        doc = DocumentModel(user_id, doc_name, result_scan)
        doc.save_to_db()
        return {"message": "Document successfully saved to Database!"}, 201


class Documents(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()

        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}

        username = UserModel.decode_user(access_token)
        docs = DocumentModel.get_all_user_docs(username)
        return {"message": "success",
                "username": username,
                "documents": docs}, 200
