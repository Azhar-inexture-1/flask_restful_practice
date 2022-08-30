from authlib.integrations.base_client import OAuthError

from core.social_auth.oauth import oauth
from core.social_auth.constants import GOOGLE_USERINFO_URL
from werkzeug.exceptions import Unauthorized, BadRequest, InternalServerError
from requests.exceptions import RequestException


class GoogleAuth:

    def __init__(self, request):
        self.request = request

    def get_data(self):
        """
        This function fetches the data from google API.
        Parameter
        ---------
        Return
        ------
        data: dict
        """
        client = oauth.create_client("google")
        if client is None:
            raise BadRequest("Google is not registered for oauth in the backend.")

        token = self.request.get_json(force=True, silent=True).get('token')
        if token is None:
            raise BadRequest("The Token is not provided.")

        client.token = token

        data = token.get('userinfo')
        if data is None:
            try:
                response = client.get(GOOGLE_USERINFO_URL, params={'skip_status': True})
            except RequestException as e:
                raise InternalServerError(f"Server failed to fetch detailed from {GOOGLE_USERINFO_URL}")
            except OAuthError as error:
                raise InternalServerError(f"Server failed to fetch detailed from {GOOGLE_USERINFO_URL}, errors: {error.error}")

            data = response.json()
            if response.status_code == 401:
                raise Unauthorized(data)
            elif response.status_code != 200:
                raise BadRequest(data)
        return data

    def auth(self):
        """
        This function handles social logins for google.
        Parameter
        ---------
        Return
        ------
        """
        data = self.get_data()
        return data
