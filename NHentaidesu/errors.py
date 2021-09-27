import typing

class NHentaiBaseErrors(Exception):
    """
    Base errors for NHentai API error.
    """

class Unauthorized(NHentaiBaseErrors):
    """
    Requested API endpoint required login.
    """
    CODE = 401

class Forbidden(NHentaiBaseErrors):
    """
    Forbidden for request to the API.
    """
    CODE = 403

class MethodNotAllowed(NHentaiBaseErrors):
    """
    Request method not allowed
    make sure request method are correct.
    """
    CODE = 405

class NotFound(NHentaiBaseErrors):
    """
    Requested endpoint doesn't exist.
    """
    CODE = 404

class TooManyRequests(NHentaiBaseErrors):
    """
    Too many requests to the API endpoint.
    """
    CODE = 429

class InternalServerError(NHentaiBaseErrors):
    """
    Requested endpoint internal error.
    """
    CODE = 500

def raise_err(status: int, msg: typing.Union[str, bool]) -> "NHentaiBaseErrors":
    if isinstance(msg, bool):
        msg = "Unknown error, maybe you already execute this before."

    if status == 401:
        err = Unauthorized(msg)
    elif status == 403:
        err = Forbidden(msg)
    elif status == 404:
        err = NotFound(msg)
    elif status == 405:
        err = MethodNotAllowed(msg)
    elif status == 429:
        err = TooManyRequests(msg)
    elif status == 500:
        err = InternalServerError(msg)
    else:
        err = NHentaiBaseErrors(msg)

    raise err