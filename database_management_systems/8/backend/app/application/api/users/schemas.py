from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str
    password: str
