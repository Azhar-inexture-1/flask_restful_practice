from core import db
from datetime import datetime
from .utils import Hasher
from core.social_auth.models import OAuthMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, data, social=False):
        self.email = data.get('email')
        if not social:
            self.password = Hasher.get_hashed_password(data.get('password'))

    @classmethod
    def save(cls, data):
        """
        Creates and saves model object.
        Parameter
        ---------
        data: Python Dictionary
            key refers to the attribute of models.
        Return
        ------
        model object
        """
        user = cls(data)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def save_social(cls, data):
        """
        Creates and saves model object when user selects social oauth service.
        Parameter
        ---------
        data: Python Dictionary
            key refers to the attribute of models.
        Return
        ------
        model object
        """
        user = cls(data, social=True)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_user_by_email(cls, email):
        """
        This method fetch user by email.
        Parameter
        ---------
        email: email of user
        return
        ------
        model object or None.
        """
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return '<{} (id: {})>'.format(type(self).__name__, self.id)


class OAuthUser(OAuthMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    def __init__(self, data, user_id, provider):
        self.email = data.get('email')
        self.provider = provider
        self.user_id = user_id
