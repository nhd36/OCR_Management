from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models.userModel import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', type=str, required=True, help='Please input your first name')
    parser.add_argument('last_name', type=str, required=True, help='Please input your last name')
    parser.add_argument('username', type=str, required=True, help='Please input your username')
    parser.add_argument('password', type=str, required=True, help='Please input your password')

    def post(self):
        data = self.parser.parse_args()
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        password = generate_password_hash(data['password'])
        existed_user = UserModel.find_user_by_username(username)
        if existed_user:
            return {"message": "Username has already existed, please try another one."}, 409
        user = UserModel(first_name, last_name, username, password)
        user.save_to_db()
        return {"message": "User registered successfully!"}, 201
