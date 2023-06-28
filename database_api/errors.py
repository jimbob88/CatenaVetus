class GenericReferencePassingError(Exception):
    """A generic exception raised when the given reference cannot be passed"""


class BookNotFoundError(GenericReferencePassingError):
    """Raised when the given book was not found"""


class ReferenceStyleNotRecognisedError(GenericReferencePassingError):
    """Raised when the reference does not match the regex style"""
