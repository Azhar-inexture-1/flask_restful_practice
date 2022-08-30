from flask import Blueprint, request
from flask_restful import Api, Resource
from core.users.services import UserServices
from flask_jwt_extended import jwt_required

errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}

users_blueprint = Blueprint('users', __name__)
users_api = Api(users_blueprint, errors=errors)


class LoginUser(Resource):
    """
    Route handles the login of user.
    Returns JWT tokens if login is successful.
    """

    login_service = UserServices(request)

    @classmethod
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        return cls.login_service.login()


class RegisterUser(Resource):
    """
    Route handles the registration of new  user.
    """

    register_service = UserServices(request)

    @classmethod
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        return cls.register_service.register()


class RefreshToken(Resource):
    """
    Generates new access token.
    Authorization is done using the refresh token.
    """

    user_service = UserServices(request)

    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        return cls.user_service.refresh_token()


# class SocialAuthUser(Resource):
#     """
#     Route handle social login and registrations.
#     """
#     auth_service = UserServices(request)
#
#     @classmethod
#     def post(cls, name):
#         """
#         This is called when request method is post.
#         Parameter
#         ---------
#         name: string
#             Name of the oauth provider
#             example:
#                 "google", "facebook", etc.
#         Return
#         ------
#         """
#         # return cls.auth_service.social_auth(name)
#         return cls.auth_service.oauth(name)


class ConnectedSocialAuth(Resource):
    """
    Generates new access token.
    Authorization is done using the refresh token.
    """

    user_service = UserServices(request)

    @classmethod
    @jwt_required()
    def get(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        return cls.user_service.get_connected_oauth()

    @classmethod
    @jwt_required()
    def delete(cls, id):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        return cls.user_service.delete_connected_oauth(id)


users_api.add_resource(RegisterUser, '/register')
# users_api.add_resource(SocialAuthUser, '/auth/<string:name>')
users_api.add_resource(LoginUser, '/login')
users_api.add_resource(RefreshToken, '/refresh')
users_api.add_resource(ConnectedSocialAuth, '/connected_oauth', '/connected_oauth/<int:id>')
