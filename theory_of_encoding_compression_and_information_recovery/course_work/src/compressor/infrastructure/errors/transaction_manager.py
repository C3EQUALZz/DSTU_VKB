from compressor.infrastructure.errors.base import InfrastructureError


class RepoError(InfrastructureError): ...


class EntityAddError(InfrastructureError): ...


class RollbackError(InfrastructureError): ...
