from flask import Blueprint, request
from flask_restful import Api, Resource
from .services import TaskServices

tasks_blueprint = Blueprint('books', __name__)
tasks_api = Api(tasks_blueprint)


class TaskResources(Resource):

    task_services = TaskServices(request)

    @classmethod
    def get(cls, id=None):
        return cls.task_services.get() if id is None else cls.task_services.get_by_id(id)

    
    @classmethod
    def post(cls):
        return cls.task_services.create()

    
    @classmethod
    def put(cls, id=None):
        return cls.task_services.update(id)


    @classmethod
    def delete(cls, id=None):
        return cls.task_services.delete(id)

tasks_api.add_resource(TaskResources, '/task', '/task/<int:id>')
