from compressor.domain.common.errors.base import DomainError


class CantDecompressThisFileError(DomainError):
    ...


class BadDataError(DomainError):
    ...
