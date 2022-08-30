GOOGLE_USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'
TWITTER_USERINFO_URL = 'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true'
GITHUB_USERINFO_URL = 'https://api.github.com/user'
GITHUB_EMAIL_URL = 'https://api.github.com/user/emails'
USERINFO_FIELDS = [
    'id', 'name', 'first_name', 'middle_name', 'last_name',
    'email', 'website', 'gender', 'locale'
]
FACEBOOK_USERINFO_ENDPOINT = 'me?fields=' + ','.join(USERINFO_FIELDS)