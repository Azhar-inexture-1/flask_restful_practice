from core import marshmallow
from .models import User
from core.constants import PASSWORD_REGEX
from marshmallow.validate import Regexp
from marshmallow import fields, validates, ValidationError


class UserSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        model = User


class UserRequestSchema(marshmallow.Schema):
    email = fields.Email(required=True, error=f"Please Enter Valid Email Address!")
    # noinspection PyTypeChecker
    password = fields.Str(
                            required=True,
                            validate=Regexp(
                                PASSWORD_REGEX, error=f"Please Enter valid Password!"
                            )
                        )


class SocialAuthUserSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        fields = ['email']

    # @validates('email')
    # def is_not_in_future(self, value):
    #     if User.query.filter(User.email == value).first() is not None:
    #         raise ValidationError("Cannot register, user with same email already exists!")
