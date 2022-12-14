from core import db
from core.users.models import User
from datetime import datetime


class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    tasks = db.relationship("Task", back_populates="task_list", cascade="all, delete-orphan")

    def __init__(self, data):
        self.title = data.get('title')
        self.user_id = data.get('user_id')

    @classmethod
    def get(cls, user_id):
        """
        This method fetch tasklist.
        Return
        ------
        tuple of model objects.
        """
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def save(cls, data):
        """
        Creates and saves model object.
        Parameter
        ---------
        data: Python Dictionary
            key refers to the attribute of models.
        Return
        ------
        model object
        """
        obj = cls(data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def get_by_id(cls, id, user_id):
        """
        This method fetch tasklist by id.
        Parameter
        ---------
        id: id of tasklist
        return
        ------
        model object or None.
        """
        return cls.query.filter_by(id=id, user_id=user_id).first()

    def update(self, data):
        """
        Used for partially updating the object.
        Parameter
        ---------
        data: Python Dictionary
            key refers to the attribute to be updated.
        Return
        ------
        model object
        """
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        return self

    def delete(self):
        """
        Deletes the objects.
        """
        db.session.delete(self)
        db.session.commit()
        return None

    def __repr__(self):
        return f'<{type(self).__name__} (id={self.id})>'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
    children = db.relationship("Task",
                               backref=db.backref('parent', remote_side=[id]),
                               cascade="all, delete-orphan"
                               )
    list_id = db.Column(db.Integer, db.ForeignKey(TaskList.id), nullable=True)
    list = db.relationship(TaskList, overlaps="tasks")
    task_list = db.relationship("TaskList", back_populates="tasks", overlaps="list")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    def __init__(self, data):
        self.title = data.get('title')
        self.user_id = data.get('user_id')
        self.list_id = data.get('list_id')
        self.parent_id = data.get('parent_id')
        self.due_date = data.get('due_date')

    @classmethod
    def get(cls, user_id):
        """
        This method fetch all tasks.
        return
        ------
        tuple of model objects.
        """
        return cls.query.filter_by(parent=None, user_id=user_id).all()

    @classmethod
    def save(cls, data):
        """
        Creates and saves model object.
        Parameter
        ---------
        data: Python Dictionary
            key refers to the attribute of models.
        Return
        ------
        model object
        """
        task = cls(data)
        db.session.add(task)
        db.session.commit()
        return task

    @classmethod
    def get_by_id(cls, id, user_id):
        """
        This method fetch task by id.
        Parameter
        ---------
        id: id of task
        return
        ------
        model object or None.
        """
        return cls.query.filter_by(id=id, user_id=user_id).first()

    def update(self, data):
        """
        Used for partially updating the object.
        Parameter
        ---------
        data: Python Dictionary
            key refers to the attribute to be updated.
        Return
        ------
        model object
        """
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        return self

    def delete(self):
        """
        Deletes the objects.
        """
        db.session.delete(self)
        db.session.commit()
        return None

    def make_parent(self):
        parent_task = Task.get_by_id(self.parent_id, self.user_id)
        self.parent_id = None
        self.list_id = parent_task.list_id
        db.session.commit()
        return self

    def switch_list(self, list_id):
        self.parent_id = None
        self.list_id = list_id
        db.session.commit()
        return self

    def __repr__(self):
        return f'<{type(self).__name__} (id={self.id})>'
