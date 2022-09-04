from .facebook import FacebookAuth
from .google import GoogleAuth
from .github import GithubAuth
from .twitter import TwitterAuth

OAuths = [
    FacebookAuth,
    GoogleAuth,
    GithubAuth,
    TwitterAuth
]

__OAUTH_MAP = {c.NAME: c for c in OAuths}


def _get_oauth_class(operator):
    return __OAUTH_MAP.get(operator)
