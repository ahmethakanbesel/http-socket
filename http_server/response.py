class HTTPResponse:
    code = 200
    name = 'OK'
    type = 'text/html'
    body = ''

    def __init__(self, response_body, status_code=200, response_type='text/html'):
        self.code = status_code
        self.type = response_type
        self.set_status_name()
        self.body = response_body
        self.print()

    def set_status_name(self):
        names = {
            200: 'OK',
            403: 'Forbidden',
            404: 'Not Found',
            400: 'Invalid Request'
        }
        self.name = names[self.code]

    def print(self):
        print(vars(self))
