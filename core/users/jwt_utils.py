import datetime

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token


class JWTAuthentication:
    """
    jwt authentication using flask-jwt
    """

    def __init__(
          self, id,
          refresh_expire_time=current_app.config.get('EXPIRE_TIME_FOR_REFRESH_TOKEN_IN_HOURS'),
          access_expire_time=current_app.config.get('EXPIRE_TIME_FOR_ACCESS_TOKEN_IN_MINUTES')):
        self.id = id
        self.refresh_timedelta = datetime.timedelta(hours=refresh_expire_time)
        self.access_timedelta = datetime.timedelta(minutes=access_expire_time)

    def create_jwt_access_token(self):
        """
        This method is used to generate the access token.
        :return: access token
        """
        return create_access_token(identity=self.id, expires_delta=self.access_timedelta)

    def create_jwt_refresh_token(self):
        """
        This method is used to create the refresh token.
        :return: refresh token
        """
        return create_refresh_token(identity=self.id, expires_delta=self.refresh_timedelta)

    def get_tokens_for_user(self):
        """
        This method is used to create the access and refresh token.
        :return: tokens
        """
        return {"access_token": self.create_jwt_access_token(),
                "refresh_token": self.create_jwt_refresh_token()}

    @staticmethod
    def decode_token(token):
        id = decode_token(token)['sub']
        return id
