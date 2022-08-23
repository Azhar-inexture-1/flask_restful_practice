from flask import Blueprint, request
from .services import GoogleAuth
from flask_restful import Api, Resource

google_blueprint = Blueprint("google", __name__)
google_api = Api(google_blueprint)


class Auth(Resource):
    """
    Route handle google login and registrations.
    """
    google = GoogleAuth(request)

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
        return cls.google.auth()


google_api.add_resource(Auth, '/auth/google')
