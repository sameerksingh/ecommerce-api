from pydantic import BaseModel, Field
import secrets

class User(BaseModel):
    email: str
    salt: str = secrets.token_hex(16)
    password: str
    role: str = Field(choices = ["Admin", "Customer"], default="Customer")


class UserInDB(User):
    id: str

