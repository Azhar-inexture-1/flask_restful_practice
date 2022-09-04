from flask import Blueprint, request
from core.social_auth.facebook.services import FacebookAuth
from core.social_auth.google.services import GoogleAuth
from core.social_auth.github.services import GithubAuth
from core.social_auth.twitter.services import TwitterAuth
from flask_restful import Api, Resource
from .services import UserServices
from ..social_auth import OAuths

social_auth_blueprint = Blueprint("social_auth", __name__)
social_auth_api = Api(social_auth_blueprint)

__OAUTH_MAP = {c.OP: c for c in OAuths}


class Facebook(Resource):
    """
    Route handle facebook login and registrations.
    """
    social_auth = FacebookAuth()

    @classmethod
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        response = cls.social_auth.auth()
        return UserServices.save_to_db(response, "facebook")


class Google(Resource):
    """
    Route handle google login and registrations.
    """
    social_auth = GoogleAuth()

    @classmethod
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        response = cls.social_auth.auth()
        return UserServices.save_to_db(response, "google")


class Twitter(Resource):
    """
    Route handle twitter login and registrations.
    """
    social_auth = TwitterAuth()

    @classmethod
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        response = cls.social_auth.auth()
        return UserServices.save_to_db(response, "twitter")


class Github(Resource):
    """
    Route handle GitHub login and registrations.
    """
    social_auth = GithubAuth()

    @classmethod
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        response = cls.social_auth.auth()
        return UserServices.save_to_db(response, "github")


social_auth_api.add_resource(Facebook, '/auth/facebook')
social_auth_api.add_resource(Google, '/auth/google')
social_auth_api.add_resource(Github, '/auth/github')
social_auth_api.add_resource(Twitter, '/auth/twitter')
