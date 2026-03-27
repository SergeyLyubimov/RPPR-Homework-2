import string
from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator, ValidationError
from typing import Self
import re

class UserRegistration(BaseModel):
    username : str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm: str = Field(min_length=8)
    age: int = Field(ge=18, le=120)
    registration_date: date = Field(default_factory=date.today)
    full_name: str = Field(min_length=2)
    phone_number: str = Field(min_length=12, max_length=12)

    @field_validator('username')
    @classmethod
    def validate_username(cls, value):
        allowed_characters = set(string.ascii_letters + string.digits + '_')
        if set(value) - allowed_characters:
            raise ValueError('Username must contain only letters, numbers and underscores')
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not (any(char.isupper() for char in value) and any(char.islower() for char in value) and any(char.isdigit() for char in value)):
            raise ValueError('Password must contain a lowercase letter, uppercase letter, and a number')
        return value

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, value):
        if not value[0].isupper():
            raise ValueError('Full name must start with a capital letter')
        return value

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        if not re.fullmatch(r'[+]\d-\d{3}-\d{2}-\d{2}', value):
            raise ValueError('Phone number must be entered in the format: +X-XXX-XX-XX')
        return value

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self

def register_user(data: dict):
    try:
        return UserRegistration(**data)
    except ValidationError as e:
        print(str(e))

register_user({'username': 'Hello',
               'email': 'insertmailhere@mail.ru',
               'password': 'InsertPasswordHere123',
               'password_confirm': 'InsertPasswordHere123',
               'age': 21,
               'full_name': 'This is a full name I guess',
               'phone_number': '+2-123-45-67'})