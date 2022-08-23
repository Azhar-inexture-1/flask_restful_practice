from flask import make_response
from http import HTTPStatus
from core.social_auth.oauth import oauth
from core.social_auth.constants import GOOGLE_OPEN_ID_URL
from core.social_auth.schemas import AuthSchema
from core.utils import Serializer

auth_schema = AuthSchema()


class GoogleAuth:

    def __init__(self, request):
        self.request = request

    def auth(self):
        """
        This function handles social logins for google.
        Parameter
        ---------
        Return
        ------
        """
        client = oauth.create_client("google")
        token = self.request.get_json(force=True, silent=True).get('token')
        if token is None:
            return make_response({
                "message": "Token is required"
            }, HTTPStatus.BAD_REQUEST)
        client.token = token
        user = token.get('userinfo')
        data = {}
        if not user:
            resp = client.get(GOOGLE_OPEN_ID_URL, params={'skip_status': True})
            print(resp.status_code)
            data = {
                'email': resp.json().get('email'),
            }
        data['provider'] = 'google'
        is_valid, data_or_errors = Serializer.load(data, auth_schema)
        return is_valid, data_or_errors
