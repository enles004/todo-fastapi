from fastapi import Query
from pydantic import BaseModel, field_validator, Field, model_validator
from datetime import datetime


class TaskPayload(BaseModel):
    title: str = Field()
    name: str = Field()
    expiry: str | None = Field()

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if len(value.split()) > 50:
            raise ValueError("Title task too long!!, max 50 letters")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value.split()) > 1000:
            raise ValueError("Name task too long!! max 1000 letters")
        return value


class TaskParams(BaseModel):
    title: str | None = None
    name: str | None = None
    action: bool | None = None
    id_task: str | None = None
    page: int = Query(default=1)
    per_page: int = Query(default=10)
    sort_by: str = Query(default="id")
    order: str = Query(default="asc")

    @model_validator(mode="after")
    def check_pagination(self):
        cr_page = self.page
        cr_per_page = self.page

        if cr_page < 0 and cr_per_page < 0:
            raise ValueError("page or per_page not less than zero!!")

        return self

    @field_validator("order")
    @classmethod
    def check_sort(cls, value):
        if value != "asc" and value != "desc":
            raise ValueError("Can only be 'asc' or 'desc'")
        return value
