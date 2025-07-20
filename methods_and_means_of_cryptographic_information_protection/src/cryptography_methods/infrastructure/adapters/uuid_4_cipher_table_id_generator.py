import uuid

from cryptography_methods.domain.cipher_table.services.id_generator import CipherTableIdGenerator
from cryptography_methods.domain.cipher_table.values.table_id import TableID


class UUID4CipherTableIdGenerator(CipherTableIdGenerator):
    async def __call__(self) -> TableID:
        return TableID(uuid.uuid4())
