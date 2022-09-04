from core.social_auth.oauth import oauth
from core.social_auth.constants import GITHUB_USERINFO_URL, GITHUB_EMAIL_URL
from werkzeug.exceptions import Unauthorized, BadRequest, InternalServerError
from requests.exceptions import RequestException
from authlib.integrations.flask_client import OAuthError
from flask import request


class GithubAuth:
    NAME = "github"

    def __init__(self):
        self.client = oauth.create_client("github")
        if not self.client:
            raise BadRequest("Github is not register for oauth in the backend.")

    def get_mail(self):
        try:
            response = self.client.get(GITHUB_EMAIL_URL)
        except RequestException as e:
            raise InternalServerError(f"Server failed to fetch detailed from {GITHUB_USERINFO_URL}")

        data = response.json()
        if response.status_code == 401:
            raise Unauthorized(data)
        elif response.status_code != 200:
            raise BadRequest(data)
        return next((item['email'] for item in data if item['primary']), None)

    def get_data(self):
        """
        This function fetches the data from github API.
        Parameter
        ---------
        Return
        ------
        data: dict
        """
        token = request.get_json(force=True, silent=True).get('token')
        if not token:
            raise BadRequest("The Token is not provided.")

        self.client.token = token

        data = token.get('userinfo')
        if not data:
            try:
                response = self.client.get(GITHUB_USERINFO_URL, params={'skip_status': True})
            except RequestException as e:
                raise InternalServerError(f"Server failed to fetch detailed from {GITHUB_USERINFO_URL}")
            except OAuthError as error:
                raise InternalServerError(f"Server failed to fetch detailed from {GITHUB_USERINFO_URL}, errors: {error.error}")
            data = response.json()
            if response.status_code == 401:
                raise Unauthorized(data)
            elif response.status_code != 200:
                raise BadRequest(data)

            if not data.get('email'):
                data['email'] = self.get_mail()

        return data

    def auth(self):
        """
        This function handles social logins for github.
        Parameter
        ---------
        Return
        ------
        """
        return self.get_data()
