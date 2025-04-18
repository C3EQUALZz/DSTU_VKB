from typing import Self

from pydantic import BaseModel, Field, model_validator


class MatrixEncodeRequestSchema(BaseModel):
    text: str = Field(default="1101", description="Обычный текст для заполнения", validate_default=True)
    matrix: list[list[int]] = Field(
        default=[
            [1, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 1, 0, 1]
        ],
        description="Матрица G для кодирования",
        validate_default=True
    )

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if len(self.text) != len(next(zip(*self.matrix))):
            raise ValueError("Количество символов для кодирования должно совпадать с количеством строк в G матрице")

        return self


class PolynomEncodeRequestSchema(BaseModel):
    text: str = Field(
        default="1101",
        description="Обычный текст для заполнения",
        validate_default=True
    )

    polynom: str = Field(
        default="(x^3 + x + 1)",
        description="Полином, с помощью которого будем кодировать и декодировать",
        validate_default=True
    )

    n: int = Field(default=7, description="Длина каждого циклического кода", validate_default=True)


class PolynomDecodeRequestSchema(PolynomEncodeRequestSchema):
    text: str = Field(
        default="1010001",
        description="Текст для декодирования",
        validate_default=True
    )


class MatrixDecodeRequestSchema(MatrixEncodeRequestSchema):
    text: str = Field(
        default="1010001",
        description="Текст для декодирования",
        validate_default=True
    )
