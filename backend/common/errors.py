class InvalidMessageError(Exception):
    pass


class RejectedMessage(Exception):
    pass


class NotFoundError(Exception):
    pass


class UnavailableError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ConflictError(Exception):
    pass


class BadRequestError(Exception):
    pass
