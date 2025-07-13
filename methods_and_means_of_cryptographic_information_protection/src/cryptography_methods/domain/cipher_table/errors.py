from cryptography_methods.domain.common.errors.base import DomainFieldError, DomainError


class NegativeTableDimensionError(DomainFieldError):
    ...


class ZeroTableDimensionError(DomainFieldError):
    ...


class TableWidthAndHeightNotDoesntMatchDataError(DomainError):
    ...


class UnknownTypeDataForCreateTableError(DomainError):
    ...


class DataCantContainBadSymbolsError(DomainError):
    ...
