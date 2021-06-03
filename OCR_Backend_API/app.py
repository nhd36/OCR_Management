from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import JWT_SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/doc_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

jwt_manager = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)


def main(ip, port):
    from models.userModel import UserModel
    from models.documentModel import DocumentModel
    from api.userResource import UserRegister, UserLogin, UserLogOut, UserProfile
    from api.documentResource import Document, Documents, DocumentReader, DocumentKeywords

    @app.before_first_request
    def before_first_request():
        db.create_all()
        print("Database generate!")

    api.add_resource(UserProfile, "/authorize_user")
    api.add_resource(UserRegister, "/register")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogOut, "/logout")
    api.add_resource(DocumentReader, "/reader")
    api.add_resource(DocumentKeywords, "/searchkeywords")
    api.add_resource(Document, "/document/<string:doc_name>")
    api.add_resource(Documents, "/documents")

    app.run(host=ip, port=port, debug=True)
