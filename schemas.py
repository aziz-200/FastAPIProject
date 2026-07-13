from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SignUpModel(BaseModel):
    # id: Optional[int]
    username: str # required
    email: EmailStr
    password: str
    is_staff: bool = Field(default=False, examples=[False])
    is_active: bool = Field(default=True, examples=[True])

    class Config:
        orm_mode = True
        schema_extra = {"example": {"username": "johndoe",
                                    "email": "john@example.com",
                                    "password": "password",
                                    "is_staff": False,
                                    "is_active": True}}
