from pydantic import BaseModel, Field


class User(BaseModel):
    email: str
    password: str
    role: str = Field(choices = ["Admin", "Customer"], default="Customer")


class UserInDB(User):
    id: str

