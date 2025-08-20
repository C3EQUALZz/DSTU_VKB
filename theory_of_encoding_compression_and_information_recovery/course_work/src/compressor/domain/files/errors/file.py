from compressor.domain.common.errors.base import DomainFieldError, DomainError


class FileSizeNegativeError(DomainFieldError):
    ...


class FileDoesntExistError(DomainError):
    ...


class UnsupportedFileObjectExtensionError(DomainFieldError):
    ...
