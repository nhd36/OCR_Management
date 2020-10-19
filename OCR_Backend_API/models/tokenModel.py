from app import db

class TokenModel(db.Model):
    __tablename__ = "tokenblock"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False)

    def __init__(self, token):
        self.token = token

    @classmethod
    def addTokenToBlackList(cls, token):
        token = cls(token)
        db.session.add(token)
        db.session.commit()

    @classmethod
    def validateTokenInBlackList(cls, token):
        existed_token = cls.query.filter_by(token=token).first()
        if existed_token:
            return True
        return False
