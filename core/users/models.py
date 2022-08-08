from core import db
from datetime import datetime
from .utils import Hasher

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, data):
        self.email = data.get('email')
        self.password = Hasher.get_hashed_password(data.get('password'))


    @classmethod
    def save(cls, data):
        user = cls(data)
        db.session.add(user)
        db.session.commit()
        return user

    
    @classmethod
    def get_user_by_email(cls, value):
        return cls.query.filter_by(email=value).first()

    def __repr__(self):
        return '<{} (id: {})>'.format(type(self).__name__, self.id)
