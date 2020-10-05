from app import db
from .userModel import UserModel

class DocumentModel(db.Model):
    __tablename__ = 'documents'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    doc_name = db.Column(db.String(50), primary_key=True)
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
        doc = cls.query.filter_by(user_id=user_id).filter_by(doc_name=doc_name).first()
        return doc

    @classmethod
    def update_doc_by_name(cls, doc_name, content, new_name, username):
        doc_exist = cls.query.filter_by(doc_name=new_name).first()
        if new_name != doc_name and doc_exist:
            return "Matched name with another document, please pick another name", 400
        doc = cls.find_doc_by_name(username, doc_name)
        doc.content = content
        doc.doc_name = new_name
        db.session.commit()
        return "Successfully update document", 202

    @classmethod
    def delete_doc(cls, username, doc_name):
        user_id = UserModel.find_user_by_username(username).id
        doc = cls.query.filter_by(user_id=user_id).filter_by(doc_name=doc_name).first()
        print(doc)
        db.session.delete(doc)
        db.session.commit()

    @classmethod
    def get_all_user_docs(cls, username):
        user = UserModel.find_user_by_username(username)
        docs = user.documents
        result = list()
        for doc in docs:
            my_doc = {"doc_name": doc.doc_name, "content": doc.content}
            result.append(my_doc)
        return result

    @classmethod
    def get_docs_by_keyword(cls, keywords, username):
        doc_contain = list()
        keywords = [word.strip() for word in keywords.split(",")]
        docs = DocumentModel.get_all_user_docs(username)
        for doc in docs:
            content = doc["content"]
            for keyword in keywords:
                if keyword in content:
                    doc_contain.append(doc)
                    break
        return doc_contain
