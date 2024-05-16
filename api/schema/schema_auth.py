from email_validator import EmailNotValidError
from pydantic import BaseModel, Field, field_validator, validate_email, model_validator


class RegisterPayload(BaseModel):
    username: str = Field(min_length=6, max_length=14, description="min = 6, max = 14")
    email: str = Field(min_length=5)
    password: str = Field(min_length=4, max_length=20, description="min = 4, max = 20")
    confirm_password: str = Field(min_length=4, max_length=20, description="input password again")

    @field_validator("email")
    @classmethod
    def validate_confirm_password(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value

    @model_validator(mode="after")
    def check_pass(self):
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 != pw2:
            raise ValueError("the password and confirm_password not equal")

        return self


class LoginPayload(BaseModel):
    email: str = Field(min_length=5)
    password: str = Field(max_length=20, min_length=6)

    @field_validator("email")
    @classmethod
    def validate_confirm_password(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value
