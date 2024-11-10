from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

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



class TeamBase(BaseModel):
    name: str = Field(..., example="Engineering Team")

class TeamCreate(TeamBase):
    pass  # Only name

class TeamResponse(TeamBase):
    id: int
    tasks: Optional[List[int]] = Field(None, example=[1, 2, 3])  # Placeholder for task IDs
    users: Optional[List[int]] = Field(None, example=[10, 11, 12])  # Placeholder for user IDs in team

    class Config:
        orm_mode = True

class TeamAddUser(BaseModel):
    user_id: int = Field(..., example=10)  # user ID to add to a team


class TeamWithUsers(TeamResponse):
    users: List['UserResponse'] = Field(..., example=[{"id": 10, "username": "johndoe"}, {"id": 11, "username": "janedoe"}])

class TeamWithTasks(TeamResponse):
    tasks: List['TaskResponse'] = Field(..., example=[{"id": 1, "title": "Task A"}, {"id": 2, "title": "Task B"}])



class TaskBase(BaseModel):
    title: str = Field(..., example="Complete project documentation")
    status_task: str = Field(..., example="In Progress")


class TaskCreate(TaskBase):
    user_id: Optional[int] = Field(None, example=1)
    team_id: Optional[int] = Field(None, example=2)


class TaskResponse(TaskBase):
    id: int
    datetime_of_creation: datetime = Field(..., example="2023-01-01T12:00:00")
    user_id: Optional[int] = Field(None, example=1)
    team_id: Optional[int] = Field(None, example=2)

    class Config:
        orm_mode = True



class TaskWithUserAndTeam(TaskResponse):
    user: Optional['UserResponse']  # This requires a UserResponse schema to be defined
    team: Optional['TeamResponse']  # This requires a TeamResponse schema to be defined


class TaskWithSpec(TaskResponse):
    task_spec: Optional['TaskSpecResponse']  # This requires a TaskSpecResponse schema to be defined



class TaskSpecBase(BaseModel):
    description: str = Field(..., example="Detailed specification for the task")


class TaskSpecCreate(TaskSpecBase):
    task_id: int = Field(..., example=1)


class TaskSpecResponse(TaskSpecBase):
    id: int
    timestamp_of_change: datetime = Field(..., example="2023-01-01T12:00:00")
    task_id: int = Field(..., example=1)

    class Config:
        orm_mode = True

class TaskSpecWithTask(TaskSpecResponse):
    task: Optional['TaskResponse']


class TaskSpecWithComments(TaskSpecResponse):
    comments: List['CommentResponse']  # Requires a CommentResponse schema



class CommentBase(BaseModel):
    text: str = Field(..., example="This is a comment on the task specification")
    user_username: str = Field(..., example="johndoe")

class CommentCreate(CommentBase):
    task_spec_id: int = Field(..., example=1)  # Required TaskSpec ID for association


class CommentResponse(CommentBase):
    id: int
    datetime_of_creation: datetime = Field(..., example="2023-01-01T12:00:00")
    task_spec_id: int = Field(..., example=1)

    class Config:
        orm_mode = True

class TaskSpecWithComments(TaskSpecResponse):
    comments: List[CommentResponse]