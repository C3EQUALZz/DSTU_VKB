from cryptography_methods.domain.common.errors.base import DomainFieldError


class CreationTimeFormatError(DomainFieldError):
    ...


class CreationTimeFutureError(DomainFieldError):
    ...


class UpdateTimeFormatError(DomainFieldError):
    ...


class UpdateTimeFutureError(DomainFieldError):
    ...


class DeleteTimeFormatError(DomainFieldError):
    ...


class DeleteTimeFutureError(DomainFieldError):
    ...


class InconsistentTimeError(DomainFieldError):
    ...