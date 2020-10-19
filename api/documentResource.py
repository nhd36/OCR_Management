from flask import request
from flask_restful import Resource, reqparse
import werkzeug
from io import BufferedReader
from side_methods import scan_OCR, allowed_file
from models.userModel import UserModel
from models.documentModel import DocumentModel
from models.tokenModel import TokenModel
import jwt
from config import (MESSAGE_NO_TOKEN_HEADER, MESSAGE_LOGGED_OUT, MESSAGE_UNREADABLE,
                    MESSAGE_TOKEN_EXPIRED, MESSAGE_DOC_EXIST, MESSAGE_DOC_NOT_FOUND,
                    MESSAGE_DOC_CREATED_SUCCESS, MESSAGE_DOC_DELETED_SUCCESS,
                    SC_NOT_FOUND, SC_BAD_REQUEST, SC_CREATE, SC_RESET_CONTENT,
                    SC_SUCCESS, SC_UNAUTHORIZED)

class Document(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new_name', type=str, help='Document name must be String')
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    parser.add_argument('content', type=str, help='Content must be String')

    def get(self, doc_name):
        headers = request.headers
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return MESSAGE_LOGGED_OUT, SC_RESET_CONTENT

        try:
            username = UserModel.decode_user(access_token)
        except:
            return MESSAGE_TOKEN_EXPIRED, SC_UNAUTHORIZED

        doc = DocumentModel.find_doc_by_name(username, doc_name)
        if doc:
            return {"status": 0,
                    "message": "success",
                    "username": username,
                    "documents": {"doc_name": doc.doc_name, "doc_content": doc.content}}, SC_SUCCESS
        return MESSAGE_DOC_NOT_FOUND, SC_NOT_FOUND


    def post(self, doc_name):
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return MESSAGE_LOGGED_OUT, SC_RESET_CONTENT

        try:
            username = UserModel.decode_user(access_token)
        except :
            return MESSAGE_TOKEN_EXPIRED, SC_UNAUTHORIZED

        data = self.parser.parse_args()
        if "content" not in data:
            return {"status": 1, "message": "No 'content' header found"}, SC_BAD_REQUEST
        doc_content = data["content"]

        user_id = UserModel.find_user_by_username(username).id
        existed_doc = DocumentModel.find_doc_by_name(username, doc_name)
        if existed_doc:
            return MESSAGE_DOC_EXIST, SC_BAD_REQUEST
        doc = DocumentModel(user_id, doc_name, doc_content)
        doc.save_to_db()

        return MESSAGE_DOC_CREATED_SUCCESS, SC_CREATE


    def delete(self, doc_name):
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return MESSAGE_LOGGED_OUT, SC_RESET_CONTENT

        try:
            username = UserModel.decode_user(access_token)
        except :
            return MESSAGE_TOKEN_EXPIRED, SC_UNAUTHORIZED

        data = self.parser.parse_args()
        doc = DocumentModel.find_doc_by_name(username, doc_name)
        if doc:
            DocumentModel.delete_doc(username, doc_name)
            return {"status": 0, "message": "Successfully delete document!"}
        return {"status": 1, "message": "Document doesn't exist"}

    def put(self, doc_name):
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return MESSAGE_LOGGED_OUT, SC_RESET_CONTENT

        username = UserModel.decode_user(access_token)
        data = self.parser.parse_args()
        if "new_name" not in data:
            return {"status": 1, "message": "No 'new_name' header found."}, SC_BAD_REQUEST
        if "content" not in data:
            return {"status": 1, "message": "No 'content' header found."}, SC_BAD_REQUEST

        file = data['file']
        new_name = data['new_name']
        doc_content = data['content']

        doc = DocumentModel.find_doc_by_name(username, doc_name)
        if doc:
            status, message, status_code = DocumentModel.update_doc_by_name(doc_name, doc_content, new_name, username)
            return {"status": status, "message": message}, status_code

        user_id = UserModel.find_user_by_username(username).id
        doc = DocumentModel(user_id, doc_name, doc_content)
        doc.save_to_db()
        return MESSAGE_DOC_CREATED_SUCCESS, SC_CREATE


class Documents(Resource):

    def get(self):
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()

        if TokenModel.validateTokenInBlackList(access_token):
            return MESSAGE_LOGGED_OUT, SC_RESET_CONTENT

        try:
            username = UserModel.decode_user(access_token)
        except :
            return MESSAGE_TOKEN_EXPIRED, SC_UNAUTHORIZED

        docs = DocumentModel.get_all_user_docs(username)
        return {"status": 0,
                "message": "success",
                "username": username,
                "documents": docs}, SC_SUCCESS


class DocumentReader(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', help="No 'file' header found")

    def post(self):
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return MESSAGE_LOGGED_OUT, SC_RESET_CONTENT

        try:
            username = UserModel.decode_user(access_token)
        except :
            return MESSAGE_TOKEN_EXPIRED, SC_UNAUTHORIZED

        data = self.parser.parse_args()
        file = data['file']

        if file is not None:
            if file.filename == '':
                return {"status": 1, "message": "No file found. Please input file"}, SC_BAD_REQUEST
        else:
            return {"status": 1, "message": "No file found. Please input file"}, SC_BAD_REQUEST

        if not allowed_file(file.filename):
            return {"status": 1, "message": "File type not support. Please input the following type: PNG, JPG, JPEG"}, SC_BAD_REQUEST

        try:
            image_file = BufferedReader(file)
            doc_content = scan_OCR(image_file)
        except:
            return MESSAGE_UNREADABLE, SC_BAD_REQUEST
        return {"status": 0, "message": "success", "doc_content": doc_content}, 200

class DocumentKeywords(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("keywords", type=str, required=True, help="No 'keywords' header found")

    def post(self):
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return MESSAGE_LOGGED_OUT, SC_RESET_CONTENT

        try:
            username = UserModel.decode_user(access_token)
        except :
            return MESSAGE_TOKEN_EXPIRED, SC_UNAUTHORIZED

        data = self.parser.parse_args()
        keywords = data['keywords']
        documents = DocumentModel.get_docs_by_keyword(keywords, username)
        return {"status": 0, "message": f"{len(documents)} documents found", "documents": documents}, SC_SUCCESS
