from core import marshmallow
from .models import Task, TaskList
from marshmallow import fields, validates_schema, ValidationError


class SubTaskSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializer for the task model.
    Used for serializing the children attribute of parent tasks.
    """
    class Meta:
        include_fk = True
        model = Task


class TaskSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializes the task objects.
    """

    class Meta:
        include_fk = True
        model = Task

    children = fields.Nested(SubTaskSchema, many=True)

    @validates_schema
    def validate_relation(self, data, **kwargs):
        """
        Validates schema of task model, task model object can only contain one of list_id or parent_id.
        Raises validation error if both or none is provided.
        """
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
    """
    Serializes the task list model objects.
    """
    class Meta:
        include_fk = True
        model = TaskList

    tasks = fields.Nested(TaskSchema, many=True)
