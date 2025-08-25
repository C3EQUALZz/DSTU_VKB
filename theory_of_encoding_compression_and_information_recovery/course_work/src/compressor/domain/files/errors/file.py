from compressor.domain.common.errors.base import DomainFieldError, DomainError


class FileSizeNegativeError(DomainFieldError):
    ...

class FileNameIsEmptyError(DomainError):
    ...


class UnsupportedFileObjectExtensionError(DomainFieldError):
    ...
