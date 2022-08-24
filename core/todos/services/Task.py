from core import db
from core.constants import CONTENT_NOT_FOUND_MESSAGE, DELETE_SUCCESSFUL_MESSAGE, CHANGED_TO_PARENT_TASK_SUCCESS, \
    CHANGED_TO_PARENT_TASK_FAILED, TASK_NOT_FOUND, SWITCH_LIST_FAILED, SWITCH_LIST_SUCCESS, LIST_NOT_FOUND
from core.todos.schemas import TaskSchema
from core.utils import Serializer
from core.todos.models import Task, TaskList
from flask import make_response
from http import HTTPStatus
from flask_jwt_extended import current_user

task_schema = TaskSchema()
task_update_request_schema = TaskSchema(partial=True)


class TaskServices:
    """
    Provides service functions to the routes.
    Handles request for Task model routes.
    """

    def __init__(self, request):
        self.request = request

    @staticmethod
    def get():
        """
        Calls the model get method and Serializes in required formate response.
        Return
        ------
        JSON Response, HTTP status code
        """
        data = Task.get(current_user.id)
        json_response = task_schema.dump(data, many=True)
        return make_response(json_response, HTTPStatus.OK)

    @staticmethod
    def get_by_id(id):
        """
        Calls the model get_by_id method and Serializes in required formate response.
        Parameter
        ---------
        id: id of the task
        Return
        ------
        JSON Response, HTTP status code
        """
        data = Task.get_by_id(id, current_user.id)
        if not data:
            return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
        json_response = task_schema.dump(data)
        return make_response(json_response, HTTPStatus.OK)

    def create(self):
        """
        Calls the model's save method.
        Return
        ------
        JSON Response, HTTP status code
        """
        data = self.request.get_json(silent=True)
        data['user_id'] = current_user.id
        is_valid, data_or_errors = Serializer.load(data, task_schema)
        if is_valid:
            response = Task.save(data_or_errors)
            json_response = task_schema.dump(response)
            return make_response(json_response, HTTPStatus.CREATED)

        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

    def update(self, id):
        """
        Calls the model update method and Serializes in required formate response.
        Parameter
        ---------
        id: id of the task
        Return
        ------
        JSON Response, HTTP status code
        """
        task = Task.get_by_id(id, current_user.id)
        data = self.request.get_json(silent=True)
        if task:
            is_valid, data_or_errors = Serializer.load(data, task_update_request_schema)
            if is_valid:
                response = task.update(data_or_errors)
                json_response = task_schema.dump(response)
                return make_response(json_response, HTTPStatus.OK)

            return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

        return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)

    @staticmethod
    def delete(id):
        """
        Calls the model's delete method.
        Parameter
        ---------
        id: id of the task
        Return
        ------
        JSON Response, HTTP status code
        """
        task = Task.get_by_id(id, current_user.id)
        if task:
            task.delete()
            return make_response(DELETE_SUCCESSFUL_MESSAGE, HTTPStatus.NO_CONTENT)

        return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)

    @classmethod
    def make_parent(cls, id):
        task = Task.get_by_id(id, current_user.id)
        if task:
            if task.parent_id:
                response = task.make_parent()
                json_response = Serializer.dump(data=response, schema=task_schema)
                return make_response({"message": CHANGED_TO_PARENT_TASK_SUCCESS, "data": json_response}, HTTPStatus.OK)
            return make_response(CHANGED_TO_PARENT_TASK_FAILED, HTTPStatus.BAD_REQUEST)

        return make_response(TASK_NOT_FOUND, HTTPStatus.NOT_FOUND)

    @classmethod
    def switch_list(cls, task_id, list_id):
        task = Task.get_by_id(task_id, current_user.id)
        if not task:
            return make_response(TASK_NOT_FOUND, HTTPStatus.NOT_FOUND)
        tasklist = TaskList.get_by_id(list_id, current_user.id)
        if not tasklist:
            return make_response(LIST_NOT_FOUND, HTTPStatus.NOT_FOUND)

        if task.list_id != list_id:
            response = task.switch_list(list_id)
            json_response = Serializer.dump(data=response, schema=task_schema)
            return make_response({"message": SWITCH_LIST_SUCCESS, "data": json_response}, HTTPStatus.OK)

        return make_response(SWITCH_LIST_FAILED, HTTPStatus.BAD_REQUEST)

