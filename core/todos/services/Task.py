from core.constants import CONTENT_NOT_FOUND_MESSAGE, DELETE_SUCCESSFUL_MESSAGE
from core.todos.schemas import TaskSchema
from core.utils import Serializer
from core.todos.models import Task
from flask import make_response
from http import HTTPStatus

task_schema = TaskSchema()
task_update_request_schema = TaskSchema(partial=True)


class TaskServices:

    def __init__(self, request):
        self.request = request

    @staticmethod
    def get():
        data = Task.get()
        json_response = task_schema.dump(data, many=True)
        return make_response(json_response, HTTPStatus.OK)

    @staticmethod
    def get_by_id(id):
        data = Task.get_by_id(id)
        if data is None:
            return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
        json_response = task_schema.dump(data)
        return make_response(json_response, HTTPStatus.OK)

    def create(self):
        data = self.request.get_json(silent=True)
        is_valid, data_or_errors = Serializer.load(data, task_schema)
        if is_valid:
            response = Task.save(data_or_errors)
            json_response = task_schema.dump(response)
            return make_response(json_response, HTTPStatus.CREATED)

        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)

    def update(self, id):
        task = Task.get_by_id(id)
        data = self.request.get_json(silent=True)
        if task:
            is_valid, data_or_errors = Serializer.load(data, task_update_request_schema)
            if is_valid:
                response = task.update(data_or_errors)
                json_response = task_schema.dump(response)
                return make_response(json_response, HTTPStatus.OK)
        
        return make_response(data_or_errors, HTTPStatus.BAD_REQUEST)
    

    @staticmethod
    def delete(id):
        task = Task.get_by_id(id)
        if task is not None:
            task.delete()
            return make_response(DELETE_SUCCESSFUL_MESSAGE, HTTPStatus.NO_CONTENT)

        return make_response(CONTENT_NOT_FOUND_MESSAGE, HTTPStatus.BAD_REQUEST)
