from abc import abstractmethod

from cryptography_methods.domain.cipher_table.values.table_id import TableID


class CipherTableIdGenerator:
    @abstractmethod
    def __call__(self) -> TableID: ...
