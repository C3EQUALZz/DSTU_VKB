from compressor.domain.common.errors.base import AppError


class TelegramPresentationError(AppError):
    ...


class DocumentNotProvidedError(TelegramPresentationError):
    ...


class AlgorithmNotProvidedError(TelegramPresentationError):
    ...


class TaskIdNotProviderError(TelegramPresentationError):
    ...


class UserCantBeNoneError(TelegramPresentationError):
    ...


class MessageCantBeNoneError(TelegramPresentationError):
    ...
