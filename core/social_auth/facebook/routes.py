from flask import Blueprint, request
from .services import FacebookAuth
from flask_restful import Api, Resource

facebook_blueprint = Blueprint("facebook", __name__)
facebook_api = Api(facebook_blueprint)


class Auth(Resource):
    """
    Route handle google login and registrations.
    """
    facebook = FacebookAuth(request)

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
        return cls.facebook.auth()


facebook_api.add_resource(Auth, '/auth/facebook')
