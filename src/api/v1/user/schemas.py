from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from api.v1.user.crypto import context


# class UserLoginSchema(BaseModel):
#   full_name: str
#  password: str


class UserSchema(BaseModel):
    id: int
    full_name: str
    email: EmailStr


class CreateUserSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str = Field(..., min_length=10, max_length=15)
    passport_number: str = Field(..., min_length=6, max_length=20)

    @field_validator("phone_number", "passport_number")
    @classmethod
    def validate_digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Должны быть только цифры")
        return v

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
