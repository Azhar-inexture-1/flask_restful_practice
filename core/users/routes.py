from flask import Blueprint, request
from flask_restful import Api, Resource
from core.users.services import UserServices

users_blueprint = Blueprint('users', __name__)
users_api = Api(users_blueprint)


class LoginUser(Resource):

    login_service = UserServices(request)

    @classmethod
    def post(cls):
        return cls.login_service.login()


class RegisterUser(Resource):

    register_service = UserServices(request)

    @classmethod
    def post(cls):
        return cls.register_service.register()


class SocialAuthUser(Resource):

    auth_service = UserServices(request)

    @classmethod
    def post(cls, name):
        return cls.auth_service.social_auth(name)


users_api.add_resource(RegisterUser, '/register')
users_api.add_resource(SocialAuthUser, '/social-auth/<string:name>')
users_api.add_resource(LoginUser, '/login')
