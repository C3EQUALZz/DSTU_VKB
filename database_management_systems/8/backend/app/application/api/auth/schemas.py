from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserLoginSchemaRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchemaResponse(BaseModel):
    access_token: str
    refresh_token: str
    email: EmailStr
    oid: str


class UserRegistrationSchemaRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRegistrationSchemaResponse(BaseModel):
    name: str
    email: EmailStr
    oid: str
