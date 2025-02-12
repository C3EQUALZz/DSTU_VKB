from app.domain.values.base import BaseValueObject


class DataMathExpression(BaseValueObject):
    value: str

    def validate(self) -> None:
        ...

    def as_generic_type(self) -> str:
        return str(self.value)