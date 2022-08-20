from core import db
from core.users.models import User


class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

    tasks = db.relationship("Task", back_populates="task_list")

    def __init__(self, data):
        self.title = data.get('title')
        self.user_id = data.get('user_id')

    @classmethod
    def get(cls):
        return cls.query.all()

    @classmethod
    def save(cls, data):
        obj = cls(data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def __repr__(self):
        return '<{} (id={})>'.format(type(self).__name__, self.id)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
    children = db.relationship("Task",
                               backref=db.backref('parent', remote_side=[id])
                               )
    list_id = db.Column(db.Integer, db.ForeignKey(TaskList.id), nullable=False)
    list = db.relationship(TaskList)

    task_list = db.relationship("TaskList", back_populates="tasks")

    def __init__(self, data):
        self.title = data.get('title')
        self.list_id = data.get('list_id')
        self.parent_id = data.get('parent_id')

    @classmethod
    def get(cls):
        return cls.query.filter_by(parent=None).all()

    @classmethod
    def save(cls, data):
        task = cls(data)
        db.session.add(task)
        db.session.commit()
        return task

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def __repr__(self):
        return '<{} (id={})>'.format(type(self).__name__, self.id)
