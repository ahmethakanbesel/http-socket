import os


def get_template(name: str):
    with open(os.path.join(os.path.dirname(__file__), './templates/' + name + '.html'), 'r') as f:
        contents = f.read()
    return contents
