from http_server import BaseHandler
from templates import get_template


class IndexHandler(BaseHandler):
    def get(self):
        self.response = get_template('base').format('Homepage', 'Homepage',
                                                    "<p>Method: GET</p><h2>Query Params</h2><pre>{}</pre>".format(
                                                        self.request['params']))
        pass

    def post(self):
        self.response = get_template('base').format('Homepage', 'Homepage',
                                                    "<p>Method: POST</p><h2>Post Fields</h2><pre>{}</pre>".format(
                                                        self.request['form']))
        pass
