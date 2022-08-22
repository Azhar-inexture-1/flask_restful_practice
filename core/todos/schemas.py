from core import marshmallow
from .models import Task, TaskList
from marshmallow import fields, validates_schema, ValidationError


class SubTaskSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        include_fk = True
        model = Task


class TaskSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        include_fk = True
        model = Task

    children = fields.Nested(SubTaskSchema, many=True)

    @validates_schema
    def validate_relation(self, data, **kwargs):
        list_id = data.get('list_id')
        parent_id = data.get('parent_id')

        if list_id is not None and parent_id is not None:
            raise ValidationError({
                "error": "Task can only have either of list_id or parent_id attribute."
            })

        if list_id is None and parent_id is None:
            raise ValidationError({
                "error": "Task should must have either of list_id or parent_id attribute."
            })


class TaskListSchema(marshmallow.SQLAlchemyAutoSchema):

    class Meta:
        include_fk = True
        model = TaskList

    tasks = fields.Nested(TaskSchema, many=True)
