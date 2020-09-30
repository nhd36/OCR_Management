from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/doc_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
api = Api(app)

def main():
    from models.userModel import UserModel
    from models.documentModel import DocumentModel
    from api.userResource import UserRegister
    from api.documentResource import Document, Documents
    api.add_resource(UserRegister, "/register")
    api.add_resource(Document, "/document/<string:username>/<string:doc_name>")
    api.add_resource(Documents, "/document/<string:username>")

    app.run(debug=True)

if __name__ == '__main__':
    main()
