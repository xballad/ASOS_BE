from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="Password")
    email: EmailStr = Field(..., example="johndoe@example.com")


class UserCreate(UserBase):
    password: str = Field(..., example="hashed_password")  # This should be hashed on the client side


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
