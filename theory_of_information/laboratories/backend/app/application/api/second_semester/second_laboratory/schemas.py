from pydantic import BaseModel


class ConvolutionalCodeSchemaRequest(BaseModel):
    data: str
    indexes: list[list[int]]

