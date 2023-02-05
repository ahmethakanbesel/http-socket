import os
import re
import socket
from concurrent.futures import ThreadPoolExecutor

from http_server.request_parser import RequestParser
from http_server.response import HTTPResponse


class HTTPServer:
    host = ""
    port = ""
    max_workers = ""
    routes = {}
    templates_dir = "./templates/"

    def __init__(self, host, port, max_workers, routes):
        self.sock = None
        self.timeout = 20
        self.host = host
        self.port = port
        self.max_workers = max_workers
        self.routes = routes

    # Function to send HTTP headers
    def send_headers(self, client_socket, response):
        client_socket.sendall(
            "HTTP/1.1 {} {}\n".format(response.code, response.name).encode('utf-8') +
            ("Content-Type: {}\n".format(response.type)).encode('utf-8') +
            "\n".encode('utf-8')
        )

    # Function to handle a client connection
    def handle_request(self, client_conn, client_addr):
        # Receives data from the client
        request = client_conn.recv(1024)
        # Convert the request to a string
        request_str = request.decode('utf-8')
        with open("request.log", "w") as file:
            # Write the string to the file
            file.write(request_str)
        # Parse request
        if request_str != "":
            parser = RequestParser(request_str)
            # Use a regular expression to extract the route from the path
            route = re.match(r'^([^\?]*)\??', parser.path).group(1)

            # Check if the route is in our routes dictionary
            if route in self.routes:
                # Call the corresponding handler function to get the response
                handler = self.routes[route](parser.parsed_request)
                response = handler.responder()
            else:
                with open(os.path.join(os.path.dirname(__file__), self.templates_dir + '404.html'), 'r') as f:
                    template = f.read()
                response = HTTPResponse(template, 404)
        else:
            response = HTTPResponse("<h1>400 Bad Request</h1>", 400)

        # Encode the response as bytes
        response_bytes = response.body.encode('utf-8')
        # Send the response to the client
        self.send_headers(client_conn, response)
        client_conn.sendall(response_bytes)
        # Close the client connection
        client_conn.close()

    # Function that runs in each thread in the thread pool
    def worker(self, conn_queue):
        # Continuously get client connections from the queue
        while True:
            # Get a client connection from the queue
            client_conn, client_addr = conn_queue.get()
            # Handle the client connection
            self.handle_request(client_conn, client_addr)

    # Function to start the server
    def start(self):
        # Create thread executor
        executor = ThreadPoolExecutor(max_workers=self.max_workers)

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set the timeout
        # self.sock.settimeout(self.timeout)
        # Bind the socket to the host and port
        self.sock.bind((self.host, self.port))
        # Start listening for incoming connections
        self.sock.listen()
        print('Server listening on {}:{}'.format(self.host, self.port))

        while True:
            # Accept incoming connections
            client_sock, client_addr = self.sock.accept()

            # Handle the request in a separate thread
            executor.submit(self.handle_request, client_sock, client_addr)
