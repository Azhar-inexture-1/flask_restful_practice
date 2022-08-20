from core import marshmallow
from .models import Task, TaskList
from marshmallow import fields


class SubTaskSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        include_fk = True
        model = Task


class TaskSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        include_fk = True
        model = Task

    children = fields.Nested(SubTaskSchema, many=True)

class TaskListSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        include_fk = True
        model = TaskList

    tasks = fields.Nested(TaskSchema, many=True)
