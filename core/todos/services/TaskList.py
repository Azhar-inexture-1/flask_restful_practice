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

    def __init__(self, request):
        self.request = request

    @staticmethod
    def get():
        data = TaskList.get()
        json_response = task_list_schema.dump(data, many=True)
        return make_response(json_response, HTTPStatus.OK)

    @staticmethod
    def get_by_id(id):
        data = TaskList.get_by_id(id)
        if data is None:
            return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
        json_response = task_list_schema.dump(data)
        return make_response(json_response, HTTPStatus.OK)

    def create(self):
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
        task = TaskList.get_by_id(id)
        if task is not None:
            task.delete()
            return make_response(DELETE_SUCCESSFUL_MESSAGE, HTTPStatus.NO_CONTENT)

        return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.BAD_REQUEST)