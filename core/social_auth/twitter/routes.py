from flask import Blueprint, request
from .services import TwitterAuth
from flask_restful import Api, Resource

twitter_blueprint = Blueprint("twitter", __name__)
twitter_api = Api(twitter_blueprint)


class Auth(Resource):
    """
    Route handle google login and registrations.
    """
    twitter = TwitterAuth(request)

    @classmethod
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        name: string
            Name of the oauth provider
            example:
                "google", "facebook", etc.
        Return
        ------
        """
        return cls.twitter.auth()


twitter_api.add_resource(Auth, '/auth/twitter')
