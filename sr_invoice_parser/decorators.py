import functools

from .exceptions import ParserParseException


def handle_exception():
    def wrapper(function):
        @functools.wraps(function)
        def inner(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                raise ParserParseException(
                    f"Failed to parse the HTML content in '{function.__name__}': {e}"
                )

        return inner

    return wrapper
