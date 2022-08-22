from marshmallow import ValidationError


class Serializer:
    """Marshmallow schemas load and dump method container.
    Responsible for serializing and deserializing of JSON data.
    Also validates the JSON data for the given model object.
    """

    @staticmethod
    def load(data, schema):
        """Loads the JSON data to model object.
        Parameters
        ----------
        data: Python dictionary
            key value pairs
            example:
                {
                    'name': 'John Doe'
                }
        schema: marshmallow schema object.
            Responsible for serializing of JSON data in model object.
            Validates the schema and returns Errors.
        Return
        ------
        boolean: True or False
        Python Dictionary of data or Error Messages
        """
        try:
            if data is None:
                data = {}
            task = schema.load(data)
            return True, task
        except ValidationError as e:
            return False, e.messages

    @staticmethod
    def dump(data, schema, extra_args=None):
        """Converts model object to JSON serializable data.
        Parameters
        ----------
        data: Python dictionary
            key value pairs
            example:
                {
                    'name': 'John Doe'
                }
        schema: marshmallow schema object.
            Responsible for serializing of JSON data in model object.
            Validates the schema and returns Errors.
        extra_args: Python dictionary
            Contains extra information to be added in response data.
        Return
        ------
        JSON serializable data.
        """
        data = schema.dump(data)
        if extra_args:
            data.update(extra_args)
        return data
