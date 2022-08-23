DELETE_SUCCESSFUL_MESSAGE = {"message": "Content deleted successful."}
CONTENT_NOT_FOUND_MESSAGE = {"message": "Content not found."}

# regex for Validation
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"

#user
MSG_LOG_IN_SUCCESSFULLY = "Successfully Logged in."
ERR_PASSWORD_INCORRECT = {"message": "Password incorrect."}
ERR_USER_WITH_EMAIL_NOT_EXISTS = {"message": "There is no user with given email"}
ERR_USER_NOT_EXISTS= {"message": "user with is {} is not exsits"}


#social auth
USER_INFO_URL = {
    'google': 'https://openidconnect.googleapis.com/v1/userinfo',
    'twitter': 'https://api.twitter.com/1.1/account/verify_credentials.json?include_email=true',
    'github': 'https://api.github.com/user'
}