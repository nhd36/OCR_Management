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
    parser.add_argument('new_name', type=str, help='Document name must be String')
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    parser.add_argument('content', type=str, help='Content must be String')

    def get(self, doc_name):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}, 205
        username = UserModel.decode_user(access_token)
        doc = DocumentModel.find_doc_by_name(username, doc_name)
        if doc:
            return {"message": "success",
                    "username": username,
                    "documents": {"doc_name": doc.doc_name, "doc_content": doc.content}}, 200
        return {"message": "Document does not exist."}, 404


    def post(self, doc_name):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}

        username = UserModel.decode_user(access_token)
        print(username)

        data = self.parser.parse_args()
        if "content" not in data:
            return {"message": "No 'content' header found"}
        doc_content = data["content"]

        user_id = UserModel.find_user_by_username(username).id
        existed_doc = DocumentModel.find_doc_by_name(username, doc_name)
        if existed_doc:
            return {"message": "Document name has already existed. Please pick another name"}, 400
        doc = DocumentModel(user_id, doc_name, doc_content)
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
        doc = DocumentModel.find_doc_by_name(username, doc_name)
        if doc:
            DocumentModel.delete_doc(username, doc_name)
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
        if "new_name" not in data:
            return {"message": "No 'new_name' header found."}
        if "content" not in data:
            return {"message": "No 'content' header found."}

        file = data['file']
        new_name = data['new_name']
        doc_content = data['content']

        doc = DocumentModel.find_doc_by_name(username, doc_name)
        if doc:
            DocumentModel.update_doc_by_name(doc_name, doc_content, new_name, username)
            return {"message": "Successfully update document!"}

        user_id = UserModel.find_user_by_username(username).id
        doc = DocumentModel(user_id, doc_name, doc_content)
        doc.save_to_db()
        return {"message": "Document successfully saved to Database!"}, 201


class Documents(Resource):

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


class DocumentReader(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', help="No 'file' header found")

    def post(self):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}

        username = UserModel.decode_user(access_token)
        data = self.parser.parse_args()
        file = data['file']

        print(file is None)

        if file is not None:
            if file.filename == '':
                return {"message": "No file found. Please input file"}, 400
        else:
            return {"message": "No file found. Please input file"}, 400

        if not allowed_file(file.filename):
            return {"message": "File type not support. Please input the following type: PNG, JPG, JPEG"}, 400

        try:
            image_file = BufferedReader(file)
            doc_content = scan_OCR(image_file)
        except:
            return {"message": "Cannot read image, please try another one!"}, 400
        return {"message": "success", "doc_content": doc_content}, 200

class DocumentKeywords(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("keywords", type=str, required=True, help="No 'keywords' header found")

    def post(self):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        if TokenModel.validateTokenInBlackList(access_token):
            return {"message": "You already logged out. Please log back in"}

        username = UserModel.decode_user(access_token)
        data = self.parser.parse_args()
        keywords = data['keywords']
        documents = DocumentModel.get_docs_by_keyword(keywords, username)
        return {"message": f"{len(documents)} documents found", "documents": documents}
