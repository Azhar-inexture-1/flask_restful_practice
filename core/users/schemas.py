from core import marshmallow
from .models import User
from core.constants import PASSWORD_REGEX
from marshmallow.validate import Regexp
from marshmallow import fields


class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializer for the user model.
    """
    class Meta:
        model = User


class UserRequestSchema(marshmallow.Schema):
    """
    User login request serializer.
    """
    email = fields.Email(required=True, error=f"Please Enter Valid Email Address!")
    # noinspection PyTypeChecker
    password = fields.Str(
                            required=True,
                            validate=Regexp(
                                PASSWORD_REGEX, error=f"Please Enter valid Password!"
                            )
                        )


class SocialAuthUserSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializer for social authentication of user.
    Contains the fields required from the oauth provider.
    """

    class Meta:
        model = User
        fields = ['email']
