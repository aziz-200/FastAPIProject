from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SignUpModel(BaseModel):
    # id: Optional[int]
    username: str # required
    email: EmailStr
    password: str
    is_staff: bool = Field(default=False, examples=[False])
    is_active: bool = Field(default=True, examples=[True])

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }
    }


class Settings(BaseModel):
    authjwt_secret_key: str = "0f5a06de53d4318e8c3d1c4fb2f8dfdd932265812538d5f54e8acdaca22f9cbc"



class LoginModel(BaseModel):
    username_or_email: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: str = Field(default="pending", examples=["pending", "in_transit", "Delivered"])
    product_id: Optional[int]
    user_id: Optional[int]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "quantity": 1,
                "order_status": "pending",
                "product_id": 1,
                "user_id": 1
            }
        }
    }

    @property
    def order_statuses(self):
        return self.order_status

class OrderStatusModel(BaseModel):
    order_status: Optional[str] = Field(default="pending", examples=["pending", "in_transit", "Delivered"])

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "order_status": "pending"
            }
        }
    }

    @property
    def order_statuses(self):
        return self.order_status
