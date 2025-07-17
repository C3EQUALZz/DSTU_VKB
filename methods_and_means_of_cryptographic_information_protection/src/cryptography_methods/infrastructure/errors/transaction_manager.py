from cryptography_methods.infrastructure.errors.base import InfrastructureError


class EntityAddError(InfrastructureError):
    ...


class RepositoryException(InfrastructureError):
    ...


class RollbackException(InfrastructureError):
    ...
