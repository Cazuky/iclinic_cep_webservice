"""
Exceptions
"""


class InvalidZipCodeFormatException(Exception):
    """
    Exception for zip codes with invalid format
    """
    pass


class PostmonZipCodeNotFound(Exception):
    """
    Exception for when the zip code is not found in Postmon's API
    """
    pass
