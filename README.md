# Multi-threaded HTTP Socket Server and HTTP Client
A socket level HTTP server and client implementation in Python.
Only GET and POST methods are implemented. Educational purposes only, not suitable for production.
## HTTP Server Usage

### Create a handler to handle incoming requests
```python
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
```

### Create a multi-threaded HTTP server and define routes

```python
from http_server import HTTPServer
from handlers import IndexHandler

example_server = HTTPServer('localhost', 8000, 5, {
  "/": IndexHandler,
})
example_server.start()
```

## HTTP Client Usage

```python
import socket
from http_client.client import get_status_code
from http_client import client, parse_response

# GET request
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
response = client.request('GET', 'localhost', 8000, '/index',
               sock)
response = parse_response(response)
# Retrieve only status code
status_code = get_status_code('GET', 'localhost', 8000, '/index')
```
## Benchmarking
A simple configuration for Locust can be found in `locustfile.py`.
If you have not installed Locust yet you can install it by
```bash
pip install locust
```
Then run `locust` command in your terminal to start Locust.
