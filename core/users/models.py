from core import db
from datetime import datetime
from .utils import Hasher
from core.social_auth.models import OAuthMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    oauth_account_id = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, data, social=False):
        self.email = data.get('email')
        self.oauth_account_id = data.get('account_id')
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
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    def __init__(self, data, user_id):
        self.email = data.get('email')
        self.provider = data.get('provider')
        self.account_id = data.get('account_id')
        self.user_id = user_id

    @classmethod
    def get(cls, user_id):
        """
        This method fetch all tasks.
        return
        ------
        tuple of model objects.
        """
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_by_id(cls, id, user_id):
        """
        This method fetch task by id.
        Parameter
        ---------
        id: id of task
        return
        ------
        model object or None.
        """
        return cls.query.filter_by(id=id, user_id=user_id).first()

    def delete(self):
        """
        Deletes the objects.
        """
        db.session.delete(self)
        db.session.commit()
        return None

    @classmethod
    def auth(cls, data):
        """
        Handles social auth, returns proper responses for user request.
        Creates user if social auth is connected for the first time.
        Parameter
        ---------
        data: Python Dict
            key pair values of user information.
        provider: string
            name of the oauth provider.
            example: "google", "github", "twitter" etc.
        return
        ------
        user object
        """
        email = data.get('email')
        account_id = data.get('account_id')
        user = None
        if email:
            user = User.query.filter_by(email=email).first()
        elif account_id:
            user = User.query.filter_by(oauth_account_id=account_id).first()
        if not user:
            user = User.save_social(data)
        oauth_user = cls(data, user.id)
        db.session.add(oauth_user)
        db.session.commit()
        return user
