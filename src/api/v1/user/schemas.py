from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator

from api.v1.user.crypto import context


class UserLoginSchema(BaseModel):
    full_name: str
    password: str


class UserSchema(BaseModel):
    id: int
    full_name: str
    email: EmailStr


class CreateUserSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str
    passport_number: str

    def set_password(self):
        self.password = context.hash(self.password)

    @model_validator(mode="after")
    def check_password(self) -> "CreateUserSchema":
        self.set_password()
        return self


class UpdateUserSchema(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    passport_number: Optional[str] = None
