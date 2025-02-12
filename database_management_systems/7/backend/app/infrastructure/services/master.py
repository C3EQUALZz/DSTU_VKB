from app.domain.entities.master import MasterEntity
from app.exceptions.infrastructure import AttributeException
from app.infrastructure.uow.master.base import MasterUnitOfWork


class MasterService:
    def __init__(self, uow: MasterUnitOfWork) -> None:
        self._uow = uow

    async def check_existence(
            self,
            name: str | None = None,
            surname: str | None = None,
            patronymic: str | None = None,
            phone_number: str | None = None,
    ) -> bool:
        if not (name and surname and patronymic or phone_number):
            raise AttributeException("oid or exchange_product_id")

        async with self._uow as uow:
            master: MasterEntity

            if name and surname and patronymic:
                master = await uow.master.get_by_full_name(name=name, surname=surname, patronymic=patronymic)
                if master:
                    return True

            if phone_number:
                master = await uow.master.get_by_phone_number(phone_number)
                if master:
                    return True

        return False