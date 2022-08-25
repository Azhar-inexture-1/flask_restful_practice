from flask import Blueprint, request
from .services import GithubAuth
from flask_restful import Api, Resource

github_blueprint = Blueprint("github", __name__)
github_api = Api(github_blueprint)


class Auth(Resource):
    """
    Route handle google login and registrations.
    """
    github = GithubAuth(request)

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
        return cls.github.auth()


github_api.add_resource(Auth, '/auth/github')
