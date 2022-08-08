from core.constants import (
    ERR_PASSWORD_INCORRECT,ERR_USER_WITH_EMAIL_NOT_EXISTS,
    MSG_LOG_IN_SUCCESSFULLY
    )
from .schemas import UserSchema, UserRequestSchema
from core.utils import Serializer
from .models import User
from flask import make_response
from http import HTTPStatus
from .utils import Hasher
from .jwt_utils import JWTAuthentication


user_schema = UserRequestSchema()
user_register_response_schema = UserSchema(load_only=('password',))
user_login_response_schema = UserSchema(load_only=('password', 'created_at'))


class UserServices:

    def __init__(self, request):
        self.request = request

    def register(self):
        data = self.request.get_json(force=True, silent=True)
        is_valid, data_or_errors = Serializer.load(data, user_schema)
        
        if is_valid:
            response = User.save(data_or_errors)
            json_response = Serializer.dump(response, user_register_response_schema)
            return make_response(json_response, HTTPStatus.CREATED)

        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

    def login(self):
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
