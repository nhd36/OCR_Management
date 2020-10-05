from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/doc_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "super-secret"

jwt_manger = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)

def main():
    from models.userModel import UserModel
    from models.documentModel import DocumentModel
    from api.userResource import UserRegister, UserLogin, UserLogOut
    from api.documentResource import Document, Documents, DocumentReader, DocumentKeywords
    db.create_all()
    api.add_resource(UserRegister, "/register")
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserLogOut, "/logout")
    api.add_resource(DocumentReader, "/reader")
    api.add_resource(DocumentKeywords, "/searchkeywords")
    api.add_resource(Document, "/document/<string:doc_name>")
    api.add_resource(Documents, "/documents")

    app.run(debug=True)

if __name__ == '__main__':
    main()
