from fastapi import Query
from pydantic import Field, BaseModel, field_validator, model_validator


class ProjectPayload(BaseModel):
    name: str = Field(min_length=6, max_length=1000)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if 6 > len(value) > 1000:
            raise ValueError("name not greater than 1000 and not less than 6")
        return value


class ProjectParams(BaseModel):
    # Filter
    name: str | None = None
    id: int | None = None
    action: bool | None = None
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

