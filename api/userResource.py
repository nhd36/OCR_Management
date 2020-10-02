from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models.userModel import UserModel
from models.tokenModel import TokenModel
from flask_jwt_extended import create_access_token
from flask import request

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Please input your username')
    parser.add_argument('password', type=str, required=True, help='Please input your password')
    parser.add_argument('first_name', type=str, required=True, help='Please input your first name')
    parser.add_argument('last_name', type=str, required=True, help='Please input your last name')


    def post(self):
        data = self.parser.parse_args()
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        password = data['password']
        existed_user = UserModel.find_user_by_username(username)
        if existed_user:
            return {"message": "Username has already existed, please try another one."}, 409
        user = UserModel(first_name, last_name, username, password)
        user.save_to_db()
        return {"message": "User registered successfully!"}, 201

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Please input your username')
    parser.add_argument('password', type=str, required=True, help='Please input your password')

    def post(self):
        data = self.parser.parse_args()
        username = data["username"]
        password = data["password"]
        verify = UserModel.account_credential(username, password)
        if not verify:
            return {"message": "Authorization failed, please try again"}, 401
        access_token = create_access_token(identity=username)
        return {"message": "Login successfully", "access_token": access_token}, 200

class UserLogOut(Resource):
    def get(self):
        if "Authorization" not in request.headers:
            return {"message": "Please included Token Headers"}
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        TokenModel.addTokenToBlackList(access_token)
        return {"message": "LogOut Successfully"}
