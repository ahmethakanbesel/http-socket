def parse_response(response: str):
    with open("response.log", "w") as file:
        # Write the string to the file
        file.write(response)
    # Split the response into a list of lines
    lines = response.split('\n\n')

    # Split the first line into a list of words
    # E.g. HTTP/1.1 200 OK
    first_line = lines[0].split()

    return {
        'version': first_line[0],
        'status_code': int(first_line[1]),
        'status': first_line[2],
        'body': lines[1]
    }
