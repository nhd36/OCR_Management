from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    documents = db.relationship('DocumentModel', back_populates='user')

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"{self.first_name}_{self.last_name}_{self.username}_{self.password}"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_user_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user:
            return user
        return None

    @classmethod
    def find_user_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None

    @classmethod
    def account_credential(cls, username, password):
        user = UserModel.find_user_by_username(username)
        if user:
            user_password = user.password
            return check_password_hash(user_password, password)
        return False

    @staticmethod
    def decode_user(jwt_token):
        decoded_jwt = jwt.decode(jwt_token, 'super-secret', algorithm='HS256')
        username = decoded_jwt['identity']
        return username
