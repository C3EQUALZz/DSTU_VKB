from cryptography_methods.domain.cipher_table.services.alphabet_creation.base import AlphabetCreationStrategy


class AlphabetCreationContext:
    def __init__(self, strategy: AlphabetCreationStrategy) -> None:
        self.strategy: AlphabetCreationStrategy = strategy

    def __call__(self, with_uppercase_symbols: bool = False) -> str:
        return self._strategy.create(with_uppercase_symbols)

    @property
    def strategy(self) -> AlphabetCreationStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, value: AlphabetCreationStrategy) -> None:
        self._strategy: AlphabetCreationStrategy = value
