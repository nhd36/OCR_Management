from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models.userModel import UserModel
from models.tokenModel import TokenModel
from flask_jwt_extended import create_access_token
from flask import request
from config import (MESSAGE_USER_EXIST, MESSAGE_USER_REGISTER_SUCCESS,
                    MESSAGE_NO_TOKEN_HEADER, MESSAGE_USER_LOGOUT_SUCCESS,
                    MESSAGE_UNEXPECTED_ERROR, SC_UNEXPECTED_ERR, MESSAGE_LOGGED_OUT,
                    MESSAGE_TOKEN_EXPIRED,MESSAGE_DOC_EXIST,
                    SC_CREATE, SC_UNAUTHORIZED, SC_SUCCESS, SC_CONFLICT, SC_RESET_CONTENT)

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
            return MESSAGE_USER_EXIST, SC_CONFLICT
        user = UserModel(first_name, last_name, username, password)
        user.save_to_db()
        return MESSAGE_USER_REGISTER_SUCCESS, SC_CREATE

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
            return {"status": 1, "message": "Authorization failed, please try again"}, SC_UNAUTHORIZED
        access_token = create_access_token(identity=username)
        return {"status": 0, "message": "Login successfully", "access_token": access_token}, SC_SUCCESS

class UserLogOut(Resource):
    def get(self):
        if "Authorization" not in request.headers:
            return MESSAGE_NO_TOKEN_HEADER, SC_UNAUTHORIZED
        access_token = request.headers["Authorization"].replace("Bearer", "").strip()
        TokenModel.addTokenToBlackList(access_token)
        return MESSAGE_USER_LOGOUT_SUCCESS, SC_SUCCESS

class UserProfile(Resource):
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

        user = UserModel.find_user_by_username(username)
        if user:
            return {"status": 0,
                    "message": f"{user.username}'s profile",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                        }}, SC_SUCCESS
        return MESSAGE_UNEXPECTED_ERROR, SC_UNEXPECTED_ERR
