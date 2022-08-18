from core import bcrypt


class Hasher:

    @staticmethod
    def verify_password(hashed_password, plain_password):
        return bcrypt.check_password_hash(hashed_password, plain_password)

    @staticmethod
    def get_hashed_password(password):
        return bcrypt.generate_password_hash(password).decode('utf8')


def normalize_userinfo(data):
    # make account data into format
    params = {
        # 'name': data['name'],
        'email': data.get('email'),
        # 'preferred_username': data.get('screen_name'),
    }
    return params


def get_github_data(client):
    response = {}
    resp = client.get('https://api.github.com/user/emails')
    for data in resp.json():
        if data['primary']:
            email = data['email']
            break
    else:
        email = None
    response['email'] = email
    return response


user_info_url = {
    'google': 'https://openidconnect.googleapis.com/v1/userinfo',
    'twitter': 'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true'
}
