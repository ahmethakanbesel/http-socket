class RequestParser:
    crlf = "\r\n\r\n"

    def __init__(self, raw_request: str):
        self.parsed_request = self.parse_request(raw_request)
        self.path = self.parsed_request['path']

    def parse_request(self, raw_request: str):
        # Split the raw request into lines
        lines = raw_request.splitlines()

        # Get the method, path, and version from the first line
        method, path, version = lines[0].split()

        # Get the query parameters from the path
        query_params = self.get_query_params(path)

        # Remove the first line from the list of lines
        lines.pop(0)

        form_values = {}
        body = None

        # Split the raw request into headers and body
        if method == "POST":
            headers, body = raw_request.split(self.crlf)

            # Get form inputs
            if body != "":
                form_values = self.get_form_values(body)

        # Return a dictionary containing the parsed request
        return {
            'method': method,
            'path': path,
            'version': version,
            # TODO: Parse HTTP headers
            # 'headers': headers,
            'params': query_params,
            'form': form_values,
            'body': body
        }

    def get_query_params(self, path: str):
        query_string = path.split('?')
        if len(query_string) > 1:
            query_string = query_string[1]
        else:
            return {}
        # Split the query string into individual parameters
        parameters = query_string.split('&')

        # Iterate over the parameters and extract the key and value
        query_params = {}
        for parameter in parameters:
            key, value = parameter.split('=')
            query_params[key] = value

        return query_params

    def get_form_values(self, body: str):
        # Split the query string into individual parameters
        parameters = body.split('&')

        # Iterate over the parameters and extract the key and value
        query_params = {}
        for parameter in parameters:
            key, value = parameter.split('=')
            query_params[key] = value

        return query_params
