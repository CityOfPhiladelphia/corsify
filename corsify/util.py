from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    '''Custom handler for regex-based routing'''
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

class InvalidUsage(Exception):
    '''Error handler that accepts a message and status code (defaults to 400)'''
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {key: getattr(self, key) for key in ['message', 'status_code']}
