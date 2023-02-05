import socket


def create_request(method, host, path):
    request_headers = '{} {} HTTP/1.1\r\nHost: {}\r\n\r\n'.format(method, path, host)

    # Print out request to console
    print('HTTP/1.1 {} {} {}'.format(method, path, host))

    return request_headers


def get_status_code(method, host, port, path, timeout=20):
    # Create a new socket
    sock = socket.socket()

    # Set the timeout
    sock.settimeout(timeout)

    # Connect to the server
    sock.connect((host, port))

    # Use the function to create an HTTP request
    request = create_request(method, host,
                             path)

    # Send request
    sock.send(request.encode())

    # Read the response
    response = sock.recv(32).decode('utf-8').splitlines()
    first_line = response[0].split()
    return int(first_line[1])


def request(method, host, port, path, sock=None, timeout=20):
    # Create a socket
    if sock is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set the timeout
    sock.settimeout(timeout)

    # Connect to a server
    sock.connect((host, port))

    # Use the function to create an HTTP request
    request = create_request(method, host,
                             path)

    # Send the request and receive the response as before
    sock.send(request.encode('utf-8'))

    # Create an empty string to store the response
    response = ''

    # Use a loop to read data from the server until there is no more data to be received
    while True:
        # Receive up to 4096 bytes of data from the server
        response_chunk = sock.recv(4096)

        # If the `recv()` method returns an empty string, break out of the loop
        if not response_chunk:
            break

        # Decode the received data from bytes to a string
        response_chunk = response_chunk.decode('utf-8')

        # Add the received data to the response string
        response += response_chunk

    # Close the socket
    sock.close()
    return response
