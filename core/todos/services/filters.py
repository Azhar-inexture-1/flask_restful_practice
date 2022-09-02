from core import query_filter
from core.constants import FILTER_MAP
from core.todos.models import Task
from ..schemas import TaskFilterSchema
from flask import request

task_schema = TaskFilterSchema()


def filter_tasks(user_id, values):
    """ This function filters task on given values
    """
    filters = [{"field": 'user_id', "op": '=', "value": user_id}, {"field": 'parent_id', "op": '=', "value": None}]

    for value in values:
        op = FILTER_MAP[value]
        val = values[value] if op != 'like' else f"%{values[value]}%"
        filter_value = {"field": value, "op": op, "value": val}
        filters.append(filter_value)
    return query_filter.search(Task, filters, task_schema)


def filter_list_tasks(tasklist_id):
    """ This function filters task on given values
    """
    filters = [{"field": 'parent_id', "op": '=', "value": None}, {"field": 'list_id', "op": '=', "value": tasklist_id}]
    values = request.args.to_dict()
    for value in values:
        op = FILTER_MAP[value]
        val = values[value] if op != 'like' else f"%{values[value]}%"
        filter_value = {"field": value, "op": op, "value": val}
        filters.append(filter_value)
    return query_filter.search(Task, filters, task_schema)
