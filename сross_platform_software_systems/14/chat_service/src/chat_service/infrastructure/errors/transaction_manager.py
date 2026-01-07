from chat_service.infrastructure.errors.base import InfrastructureError


class RepoError(InfrastructureError): ...


class EntityAddError(InfrastructureError): ...


class RollbackError(InfrastructureError): ...
