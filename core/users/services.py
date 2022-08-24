from core.constants import (
    ERR_PASSWORD_INCORRECT, ERR_USER_WITH_EMAIL_NOT_EXISTS,
    MSG_LOG_IN_SUCCESSFULLY, USER_INFO_URL
)
from core.social_auth.oauth import oauth
from .schemas import UserSchema, UserRequestSchema, SocialAuthUserSchema
from core.utils import Serializer
from .models import User, OAuthUser
from flask import make_response
from http import HTTPStatus
from .utils import Hasher
from .jwt_utils import JWTAuthentication
from flask_jwt_extended import get_jwt_identity

user_schema = UserRequestSchema()
user_register_response_schema = UserSchema(load_only=('password',))
user_login_response_schema = UserSchema(load_only=('password', 'created_at'))
social_auth_user_schema = SocialAuthUserSchema()


class UserServices:

    def __init__(self, request):
        self.request = request

    def register(self):
        """
        Registers new user using information and password.
        """
        data = self.request.get_json(force=True, silent=True)
        is_valid, data_or_errors = Serializer.load(data, user_schema)

        if is_valid:
            response = User.save(data_or_errors)
            json_response = Serializer.dump(response, user_register_response_schema)
            return make_response(json_response, HTTPStatus.CREATED)

        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

    def social_auth(self, name):
        """
        This function handles social logins.
        Parameter
        ---------
        name: String
            Name of the oauth provider
            example: "google", "twitter", etc.
        """
        client = oauth.create_client(name)
        if client is None:
            return make_response({"error": "Invalid Request"}, HTTPStatus.BAD_REQUEST)

        token = self.request.get_json(force=True, silent=True).get('token')
        if token is None:
            return make_response({"message": "Token is required"}, HTTPStatus.BAD_REQUEST)

        client.token = token
        data = token.get('userinfo')

        if data is None:
            response = client.get(USER_INFO_URL[name], params={'skip_status': True})
            response_data = response.json()
            if response.status_code != 200:
                return make_response(response_data, HTTPStatus.BAD_REQUEST)
            data = {'email': response_data.get('email'), 'account_id': str(response_data.get('id'))}

        data['provider'] = name

        # validating and storing userinfo to database
        is_valid, data_or_errors = Serializer.load(data, social_auth_user_schema)
        if is_valid:
            status, message, user = OAuthUser.auth(data_or_errors)
            if status:
                tokens = JWTAuthentication(user.id).get_tokens_for_user()
                response_data = Serializer.dump(data=user,
                                                schema=user_login_response_schema,
                                                extra_args=tokens)
                return make_response({
                    "message": message,
                    "data": response_data
                }, HTTPStatus.OK)
            return make_response({
                "message": message['message'],
            }, HTTPStatus.BAD_REQUEST)
        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

    def login(self):
        """
        This function handles the login of user.
        Return
        JWT tokens if login is successful else return respective error and status code.
        """
        data = self.request.get_json(force=True, silent=True)
        is_valid, data_or_errors = Serializer.load(data, user_schema)

        if is_valid:
            if user := User.get_user_by_email(data_or_errors.get('email')):
                if Hasher.verify_password(user.password, data_or_errors.get('password')):
                    tokens = JWTAuthentication(user.id).get_tokens_for_user()
                    response_data = Serializer.dump(data=user,
                                                    schema=user_login_response_schema,
                                                    extra_args=tokens)
                    return make_response({
                        "message": MSG_LOG_IN_SUCCESSFULLY,
                        "data": response_data
                    }, HTTPStatus.OK)
                return make_response(ERR_PASSWORD_INCORRECT, HTTPStatus.UNAUTHORIZED)
            return make_response(ERR_USER_WITH_EMAIL_NOT_EXISTS, HTTPStatus.FORBIDDEN)
        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

    @staticmethod
    def refresh_token():
        """
        Generates new access token.
        Parameter
        ---------
        Return
        ------
        {message, access_token}, http status code
        """
        identity = get_jwt_identity()
        access_token = JWTAuthentication(identity).create_jwt_access_token()
        return make_response(
            {
                "message": "Successful.",
                "access_token": access_token
            }, HTTPStatus.OK)
