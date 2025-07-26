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


class OnlyLettersCanBeInKeyError(DomainFieldError):
    ...


class StringContainsCharactersFromDifferentAlphabetsError(DomainFieldError):
    ...


class TableSizesDoNotMatchError(DomainError):
    ...


class CantFindSymbolInTableError(DomainError):
    ...
