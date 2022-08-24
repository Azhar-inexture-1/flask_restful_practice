from flask import make_response
from http import HTTPStatus
from core.social_auth.oauth import oauth
from core.social_auth.constants import GOOGLE_OPEN_ID_URL
from core.social_auth.schemas import AuthSchema

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
        if client is None:
            return {"error": "Invalid Request"}

        token = self.request.get_json(force=True, silent=True).get('token')
        if token is None:
            return {"error": "Token is required"}

        client.token = token

        data = token.get('userinfo')
        if data is None:
            response = client.get(GOOGLE_OPEN_ID_URL, params={'skip_status': True})
            response_data = response.json()
            if response.status_code != 200:
                return make_response(response_data, HTTPStatus.BAD_REQUEST)

            data = {'email': response_data.get('email'), 'account_id': str(response_data.get('id'))}

        data['provider'] = 'google'
        return data
