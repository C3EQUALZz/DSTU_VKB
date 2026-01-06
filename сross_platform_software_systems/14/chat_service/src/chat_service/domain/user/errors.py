from chat_service.domain.common.errors.base import DomainFieldError, DomainError


class BadAPIKeyError(DomainFieldError):
    ...


class RoleChangeNotPermittedError(DomainError): ...


class ActivationChangeNotPermittedError(DomainError): ...


class AuthorizationError(DomainError): ...
