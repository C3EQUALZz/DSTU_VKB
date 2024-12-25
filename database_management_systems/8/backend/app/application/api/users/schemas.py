from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str


class UpdateUserSchema(BaseModel):
    name: str
    email: str
    password: str


class ErrorMessageScheme(BaseModel):
    error: str
