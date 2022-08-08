from core import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, data):
        self.name = data.get('name')

    @classmethod
    def get(cls):
        return cls.query.all()

    @classmethod
    def save(cls, data, *args):
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
