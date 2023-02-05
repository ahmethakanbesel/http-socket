from .response import HTTPResponse


class BaseHandler:
    content_type = 'text/html'
    status = 200

    # Method to handle requests to a specific route
    def __init__(self, request):
        self.request = request
        self.response = ""
        self.content_type = 'text/html'
        self.status = 200
        print(self.request)

    def get(self):
        pass

    def post(self):
        pass

    def responder(self):
        if self.request['method'] == 'GET':
            self.get()
        elif self.request['method'] == 'POST':
            self.post()
        return HTTPResponse(self.response, self.status, self.content_type)
        pass
