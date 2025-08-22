from compressor.application.errors.base import ApplicationError


class UserNotFoundError(ApplicationError):
    ...


class UserAlreadyExistsError(ApplicationError):
    ...
