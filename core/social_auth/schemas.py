from core import marshmallow
from marshmallow import fields


class AuthSchema(marshmallow.Schema):
    """
    Serializer for oauth model.
    """
    provider = fields.Str(required=True)
    account_id = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)


