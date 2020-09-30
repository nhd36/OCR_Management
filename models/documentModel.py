from app import db
from .userModel import UserModel

class DocumentModel(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doc_name = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('UserModel', back_populates='documents')

    def __init__(self, user_id, doc_name, content):
        self.user_id = user_id
        self.doc_name = doc_name
        self.content = content

    def __repr__(self):
        return f"{self.user_id}_{self.doc_name}_{self.content}"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_doc_by_name(cls, username, doc_name):
        user_id = UserModel.find_user_by_username(username).id
        docs = cls.query.filter_by(user_id=user_id).filter_by(doc_name=doc_name).all()
        result = list()
        for doc in docs:
            my_doc = {"doc_id": doc.id, "doc_name": doc.doc_name, "content": doc.content}
            result.append(my_doc)
        return result

    @classmethod
    def find_doc_by_id(cls, username, doc_id):
        user_id = UserModel.find_user_by_username(username).id
        doc = cls.query.filter_by(user_id=user_id).filter_by(id=doc_id).first()
        return doc

    @classmethod
    def update_doc_by_id(cls, username, doc_id, content, new_name):
        doc = cls.find_doc_by_id(username, doc_id)
        doc.content = content
        doc.doc_name = new_name
        db.session.commit()

    @classmethod
    def delete_doc(cls, username, doc_name, doc_id):
        user_id = UserModel.find_user_by_username(username).id
        doc = cls.query.filter_by(user_id=user_id).filter_by(id=doc_id).first()
        db.session.delete(doc)
        db.session.commit()

    @classmethod
    def get_all_user_docs(cls, username):
        user = UserModel.find_user_by_username(username)
        docs = user.documents
        result = list()
        for doc in docs:
            my_doc = {"doc_id": doc.id, "doc_name": doc.doc_name, "content": doc.content}
            result.append(my_doc)
        return result
