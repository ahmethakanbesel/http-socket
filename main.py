from http_server import HTTPServer
from handlers import IndexHandler
from settings import SW_PORT, THREAD_COUNT, HOSTNAME

example_server = HTTPServer(HOSTNAME, SW_PORT, THREAD_COUNT, {
    "/": IndexHandler,
})
example_server.start()
