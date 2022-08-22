from flask import Blueprint, request
from flask_restful import Api, Resource
from .services import TaskServices, TaskListServices
from flask_jwt_extended import jwt_required


tasks_blueprint = Blueprint('books', __name__)
tasks_api = Api(tasks_blueprint)


class TaskResources(Resource):

    task_services = TaskServices(request)

    @classmethod
    @jwt_required()
    def get(cls, id=None):
        """
        This is called when request method is get.
        Parameter
        ---------
        id: id of task
        Return
        ------
        """
        return cls.task_services.get() if id is None else cls.task_services.get_by_id(id)

    @classmethod
    @jwt_required()
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        return cls.task_services.create()
    
    @classmethod
    @jwt_required()
    def put(cls, id=None):
        """
        This is called when request method is put.
        Parameter
        ---------
        id: id of task
        Return
        ------
        """
        return cls.task_services.update(id)

    @classmethod
    @jwt_required()
    def delete(cls, id=None):
        """
        This is called when request method is delete.
        Parameter
        ---------
        id: id of task
        Return
        ------
        """
        return cls.task_services.delete(id)


class TaskListResources(Resource):
    task_list_services = TaskListServices(request)

    @classmethod
    @jwt_required()
    def get(cls, id=None):
        """
        This is called when request method is get.
        Parameter
        ---------
        id: id of task
        Return
        ------
        """
        return cls.task_list_services.get() if id is None else cls.task_list_services.get_by_id(id)

    @classmethod
    @jwt_required()
    def post(cls):
        """
        This is called when request method is post.
        Parameter
        ---------
        Return
        ------
        """
        return cls.task_list_services.create()

    @classmethod
    @jwt_required()
    def put(cls, id=None):
        """
        This is called when request method is put.
        Parameter
        ---------
        id: id of task
        Return
        ------
        """
        return cls.task_list_services.update(id)

    @classmethod
    @jwt_required()
    def delete(cls, id=None):
        """
        This is called when request method is delete.
        Parameter
        ---------
        id: id of task
        Return
        ------
        """
        return cls.task_list_services.delete(id)


tasks_api.add_resource(TaskResources, '/task', '/task/<int:id>')
tasks_api.add_resource(TaskListResources, '/task_list', '/task_list/<int:id>')
