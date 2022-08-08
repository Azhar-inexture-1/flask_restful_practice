from marshmallow import ValidationError

class Serializer:

    @staticmethod
    def load(data, schema):
        try:
            if data is None:
                data = {}
            task = schema.load(data)
            return True, task
        except ValidationError as e:
            return False, e.messages

    @staticmethod
    def dump(data, schema, extra_args=None):
        data = schema.dump(data)
        if extra_args:
            data.update(extra_args)
        return data
