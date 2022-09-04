from flask import request

from core import marshmallow, query_filter
from .models import Task, TaskList
from marshmallow import fields, validates_schema, ValidationError
from flask_jwt_extended import current_user

from ..constants import FILTER_MAP


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

        if list_id and parent_id:
            raise ValidationError({
                "error": "Task can only have either of list_id or parent_id attribute."
            })

        if not list_id and not parent_id:
            raise ValidationError({
                "error": "Task should must have either of list_id or parent_id attribute."
            })

        if list_id:
            tasklist = TaskList.get_by_id(list_id, current_user.id)
            if not tasklist:
                raise ValidationError({
                    "error": {
                        "list_id": "Invalid list_id, value does not exists"
                    }
                })
        else:
            task = Task.get_by_id(parent_id, current_user.id)
            if not task:
                raise ValidationError({
                    "error": {
                        "parent_id": "Invalid parent_id, value does not exists"
                    }
                })


class ChildTaskFilterSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializes the filtering the tasks.
    """

    class Meta:
        model = Task
        include_fk = True
        fields = ['title', 'due_date', "completed", "user_id"]


class TaskFilterSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializes the filtering the tasks.
    """

    class Meta:
        model = Task
        include_fk = True
        fields = ['id', 'title', 'due_date', "completed", "user_id", "children", "parent_id", "list_id"]

    children = fields.Nested(SubTaskSchema, many=True)


task_schema = TaskFilterSchema()


class TaskListSchema(marshmallow.SQLAlchemyAutoSchema):
    """
    Serializes the task list model objects.
    """
    tasks = fields.Method("get_tasks")

    class Meta:
        include_fk = True
        model = TaskList

    # tasks = fields.Nested(TaskFilterSchema, many=True)

    def get_tasks(self, obj):
        filters = [{"field": 'parent_id', "op": '=', "value": None}, {"field": "list_id", "op": '=', "value": obj.id}]
        values = request.args.to_dict()
        for value in values:
            op = FILTER_MAP[value]
            val = values[value] if op != 'like' else f"%{values[value]}%"
            filter_value = {"field": value, "op": op, "value": val}
            filters.append(filter_value)
        return task_schema.dump(query_filter.search(Task, filters, task_schema), many=True)


class TaskUpdateSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        fields = ['title', 'due_date', "completed"]
