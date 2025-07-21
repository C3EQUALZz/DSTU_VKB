import uuid
from typing_extensions import override
from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.values.table_id import TableID


class UUID4CipherTableIdGenerator(CipherTableIdGenerator):
    @override
    def __call__(self) -> TableID:
        return TableID(uuid.uuid4())
