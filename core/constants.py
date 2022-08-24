DELETE_SUCCESSFUL_MESSAGE = {"message": "Content deleted successful."}
CONTENT_NOT_FOUND_MESSAGE = {"message": "Content not found."}

# regex for Validation
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"

# user
MSG_LOG_IN_SUCCESSFULLY = "Successfully Logged in."
ERR_PASSWORD_INCORRECT = {"message": "Password incorrect."}
ERR_USER_WITH_EMAIL_NOT_EXISTS = {"message": "There is no user with given email"}
ERR_USER_NOT_EXISTS = {"message": "user with is {} is not exists"}
PASSWORD_LOGIN_REQUIRED = {'message': 'Please use password to login!'}


def oauth_login_mismatch(provider):
    return {'message': f"Same user is registered with {provider}, please login using \
{provider}"}


# social auth
USER_INFO_URL = {
    'google': 'https://openidconnect.googleapis.com/v1/userinfo',
    'twitter': 'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
    'github': 'https://api.github.com/user'
}

# todo
TASK_NOT_FOUND = {"message": "Task not found."}
LIST_NOT_FOUND = {"message": "List not found."}
CHANGED_TO_PARENT_TASK_SUCCESS = "Task is successfully changed to parent task."
CHANGED_TO_PARENT_TASK_FAILED = {"message": "Task is already a parent task."}
SWITCH_LIST_SUCCESS = "Task is successfully switched to the given list."
SWITCH_LIST_FAILED = {"message": "Task is already in the same list."}
