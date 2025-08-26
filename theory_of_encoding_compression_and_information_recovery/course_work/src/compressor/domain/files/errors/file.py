from compressor.domain.common.errors.base import DomainError, DomainFieldError


class FileSizeNegativeError(DomainFieldError):
    ...

class FileNameIsEmptyError(DomainError):
    ...


class UnsupportedFileObjectExtensionError(DomainFieldError):
    ...
