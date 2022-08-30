from core import marshmallow
from .models import User, OAuthUser
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

    provider = fields.Str(required=True)
    account_id = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)


class OAuthUserSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializer for social authentication of user.
    """
    class Meta:
        model = OAuthUser
        include_fk = True
