from core import marshmallow
from .models import Task


class TaskSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        model = Task
