from typing import List, Literal, Any

from pydantic import BaseModel, Field, model_validator
from pydantic_core import from_json


class JsonStringModel(BaseModel):
    """`BaseModel` subclass used to validate objects passed to API as JSON strings.

    The primary use case is treating one of the form fields as JSON payload. We need to do that
    in case of endpoints that accept both file and rich set of input parameters. We cannot receive
    both file and JSON body because they use conflicting Content-Type header. It is
    "multipart/form-data" for the former and "application/json" for the latter. If we require
    a client to send a file, we have to use the data sent in form for input parameters.

    Theoretically we could use several form fields to gather all the required input parameters.
    However, some of them are nested in their nature and forms don't support that. That's why we
    consider it better to just use one form field and process its content as JSON payload.

    If a form field model inherits from this class, we will get API documentation and input
    validation - just the way we get it for JSON body defined with `BaseModel`.
    """

    @model_validator(mode="before")
    @classmethod
    def convert_json_string_into_dictionary(cls, data: Any) -> Any:
        if isinstance(data, str):
            try:
                return from_json(data)
            except ValueError as e:
                raise ValueError("Input should be a valid JSON string") from e
        return data


class EncodeCascadeCodeRequestSchema(JsonStringModel):
    matrix: List[List[int]] = Field(
        default=[
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 1]
        ],
        description="Матрица для блочного кода",
        validate_default=True
    )

    type_matrix: Literal["G", "H"] = Field(
        default="G",
        description="Тип матрицы для блочного кода",
        validate_default=True
    )

    indexes: list[list[int]] = Field(
        default=[
            [0, 2, 3],
            [1, 2],
            [0, 3]
        ],
        description="Индексы для сумматоров",
        validate_default=True
    )


class DecodeCascadeCodeRequestSchema(BaseModel):
    matrix: List[List[int]] = Field(
        default=[
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 1],
            [0, 1, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 1]
        ],
        description="Матрица для блочного кода",
        validate_default=True
    )

    type_matrix: Literal["G", "H"] = Field(
        default="G",
        description="Тип матрицы для блочного кода",
        validate_default=True
    )

    data: str

    indexes: list[list[int]] = Field(
        default=[
            [0, 2, 3],
            [1, 2],
            [0, 3]
        ],
        description="Индексы для сумматоров",
        validate_default=True
    )

    image_width: int = Field(default=20, description="Ширина изображения")
    image_height: int = Field(default=29, description="Высота изображения")