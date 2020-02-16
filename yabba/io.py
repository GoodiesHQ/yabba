import aiohttp
from yabba.utils import trycast


################
#   File I/O   #
################

def read_lines(filename: str, encoding: str = "utf-8"):
    with open(filename, "r", encoding=encoding) as f:
        for line in f:
            yield line.strip()


def read_lines_delim(filename: str, delim: str = '::', expected_length: int = None, encoding="utf-8"):
    for line in read_lines(filename, encoding):
        data = line.split(delim)
        if expected_length is None or len(data) == expected_length:
            yield data


def target_factory(filename: str, default_port: int, encoding: str = "utf-8"):
    def wrapper():
        for line in read_lines(filename):
            if ':' in line:
                line = line.split(':')
                yield line[0], trycast(int, line[1], default_port)
            else:
                yield line, default_port
    return wrapper


def combo_factory(filename: str, delim: str = "::", encoding="utf-8"):
    def wrapper():
        for creds in read_lines_delim(filename, delim, encoding):
            yield creds
    return wrapper


def value_factory(values):
    values = list(values)
    def wrapper():
        nonlocal values
        for value in values:
            yield value
    return wrapper


################
#   HTTP I/O   #
################
