# Exception Classes for Error-Handling


class InvalidUserInput(Exception):
    """
    InvalidUserInput raises an error if the user does not input a city, state or city, country
    """

    pass


class APIError(Exception):
    """
    APIError raises an error if there is an error communicating with the API
    """

    pass


class IndexError(Exception):
    """
    IndexError Raises an error if the index is out of range due to a user error.
    """

    pass
