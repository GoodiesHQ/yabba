from urllib.parse import urlparse
from yabba.utils import trycast
import aiohttp


__all__ = [
    "read_lines", "read_lines_delim", "ssh_target_factory",
    "http_target_factory", "combo_factory", "line_factory", "value_factory",
]

_schemes = dict(http="http://", https="https://")


################
#   File I/O   #
################

def read_lines(filename: str, encoding: str = "utf-8"):
    with open(filename, "r", encoding=encoding) as f:
        for line in f:
            yield line.strip()


def read_lines_delim(filename: str,
                     delim: str = '::',
                     expected_length: int = None,
                     encoding="utf-8"):
    for line in read_lines(filename, encoding):
        data = line.split(delim)
        if expected_length is None or len(data) == expected_length:
            yield data


def ssh_target_factory(filename: str,
                       default_port: int,
                       encoding: str = "utf-8"):
    def wrapper():
        for line in read_lines(filename):
            if ':' in line:
                line = line.split(':')
                yield line[0], trycast(int, line[1], default_port)
            else:
                yield line, default_port
    return wrapper


def http_target_factory(filename: str,
                        default_scheme: str,
                        encoding: str = "utf-8"):
    pfx = _schemes["https"] if default_scheme.lower().startswith("https") \
          else _schemes["http"]

    def wrapper():
        for line in read_lines(filename):
            if not any(map(line.startswith, _schemes)):
                line = pfx + line
            try:
                url = urlparse(line)
            except Exception as e:
                print(type(e), e, sep="\n")
            else:
                yield (url.geturl(),)

    return wrapper


def line_factory(filename: str, encoding: str = "utf-8"):
    def wrapper():
        for line in read_lines(filename, encoding):
            yield line
    return wrapper


def combo_factory(filename: str, delim: str = "::", encoding: str = "utf-8"):
    def wrapper():
        for creds in read_lines_delim(filename, delim, 2, encoding):
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
