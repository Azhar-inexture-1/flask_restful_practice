from core.constants import CONTENT_NOT_FOUND_MESSAGE, DELETE_SUCCESSFUL_MESSAGE
from core.todos.schemas import TaskListSchema
from core.utils import Serializer
from core.todos.models import TaskList
from flask import make_response
from http import HTTPStatus
from flask_jwt_extended import current_user

task_list_schema = TaskListSchema()
task_list_update_request_schema = TaskListSchema(partial=True)


class TaskListServices:
    """
    Provides service functions to the routes.
    Handles request for Task List model routes.
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
        data = TaskList.get(current_user.id)
        json_response = task_list_schema.dump(data, many=True)
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
        data = TaskList.get_by_id(id, current_user.id)
        if data is None:
            return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
        json_response = task_list_schema.dump(data)
        return make_response(json_response, HTTPStatus.OK)

    def create(self):
        """
        Calls the model's save method.
        Return
        ------
        JSON Response, HTTP status code
        """
        data = self.request.get_json(force=True, silent=True)
        data['user_id'] = current_user.id
        is_valid, data_or_errors = Serializer.load(data, task_list_schema)
        print(is_valid)
        if is_valid:
            response = TaskList.save(data_or_errors)
            json_response = task_list_schema.dump(response)
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
        task = TaskList.get_by_id(id)
        data = self.request.get_json(silent=True)
        if task:
            is_valid, data_or_errors = Serializer.load(data, task_list_update_request_schema)
            if is_valid:
                response = task.update(data_or_errors)
                json_response = task_list_schema.dump(response)
                return make_response(json_response, HTTPStatus.OK)

        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

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
        task = TaskList.get_by_id(id)
        if task is not None:
            task.delete()
            return make_response(DELETE_SUCCESSFUL_MESSAGE, HTTPStatus.NO_CONTENT)

        return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.BAD_REQUEST)
