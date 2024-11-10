from datetime import datetime
from tkinter.scrolledtext import example
from typing import Optional

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

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="johndoe@example.com")  # Using email for login
    password: str = Field(..., example="Password123")

class CreateTask(BaseModel):
    email_creator: EmailStr = Field(..., example="johndoe@example.com")  # Using email for login
    title: str = Field(..., example="Nazov tasku")
    description : str = Field(..., example="Description tasku")
    status_task: str = Field(..., example="Faza tasku")
    email_assigned: EmailStr = Field(..., example="johndoe@example.com")
    team_assigned: int = Field(..., example="Nazov teamu")

class GetListOfTasksForUser(BaseModel):
    email_user: EmailStr = Field(..., example="johndoe@example.com")  # Using email for login

class TaskWithSpec(BaseModel):
    id: int = Field(..., example="Dake cislo")
    title: str = Field(..., example="Titulok")
    status_task: str = Field(..., example="Status Tasku")
    description: Optional[str] = Field(None, example="Popis")  # Make description optional
    datetime_of_creation: datetime = Field(..., example="cas ?")