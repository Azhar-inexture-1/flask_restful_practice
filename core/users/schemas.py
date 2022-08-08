from core import marshmallow
from .models import User
from core.constants import PASSWORD_REGEX
from marshmallow.validate import Regexp
from marshmallow import fields


class UserSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        model = User


class UserRequestSchema(marshmallow.Schema):
    email = fields.Email(required=True, error=f"Please Enter Valid Email Address!")
    password = fields.Str(
                                    required=True,
                                    validate=Regexp(
                                        PASSWORD_REGEX, error=f"Please Enter valid Password!"
                                    )
                                )
