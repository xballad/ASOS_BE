import string

from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from db.dependencies import get_db
from jwtS.workToken import create_access_token, verify_token
from schemas import UserCreate, UserResponse, UserLogin, CreateTask, GetListOfTasksForUser, TaskWithSpec, \
    ForgotPasswordRequest
from db.crud import *
from db.db import init_db
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import bcrypt
import random
from scripts.scriptMail import send_email

app = FastAPI(
    title="Task Managment APP",
    description="API for managing user registrations and data",
    version="1.0.0",
    contact={"name": "ASOS-team", "email": "lore@ipsum.sk"}
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allows Angular app to access backend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

#INNIT DB
init_db()
#overovanie hesiel
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/register", response_model=UserResponse, tags=["User Registration"], summary="Register a new user")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email is already in use")

    # Generate salt and hash password using bcrypt
    salt = bcrypt.gensalt()  # Generate a salt using bcrypt
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)  # Hash the password with the salt

    # Store both hashed password and salt in the database
    db_user = create_user(db, name=user.name, last_name=user.last_name,
                          username=user.username, password=hashed_password.decode('utf-8'),
                          salt=salt.decode('utf-8'), email=user.email)

    return db_user  # Return the created user


@app.post("/api/login", tags=["User Authentication"], summary="Login a user")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    salt = db_user.salt.encode('utf-8')
    stored_hashed_password = db_user.password.encode('utf-8')
    provided_hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)

    if provided_hashed_password != stored_hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})  # 'sub' is the subject (email)

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/forgot-password", tags=["User"])
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    salt = bcrypt.gensalt()  # Generate a salt using bcrypt
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)  # Hash the password with the salt

    update_user_password(db,
                         user_id=user.id,
                         password=hashed_password.decode('utf-8'))

    update_user_salt(db,
                     user_id=user.id,
                     salt=salt.decode('utf-8'))


    send_email(to_email=user.email, new_password=new_password)

    return {"message": "New password has been sent to your email."}



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
@app.get("/api/dashboard")
async def dashboard(token: str = Depends(oauth2_scheme)):
    # Validate the token
    payload = verify_token(token)
    user_email = payload.get("sub")  # Extract the 'sub' (email) from the token payload

    # You can fetch the user from the database using the email if needed
    # db_user = get_user_by_email(db, user_email)

    return {"message": f"Welcome to the dashboard, {user_email}!"}

@app.post("/api/create/task", tags=["Task Creation"], summary="Create a new task")
async def create_task_ep(taskform : CreateTask,db: Session = Depends(get_db)):
    task_creator = get_user_by_email(db, taskform.email_creator)

    new_task = create_task(db=db,
                           title=taskform.title,
                           status_task=taskform.status_task,
                           user_id=task_creator.id)

    new_task_spec = create_task_spec(db=db,
                                     task_id=new_task.id,
                                     description=taskform.description)

    return new_task


@app.post("/api/get/user/tasks", response_model=List[TaskWithSpec], tags=["USER Task Listing"],
            summary="List all tasks")
async def list_tasks(frompage: GetListOfTasksForUser, db: Session = Depends(get_db)):
    # Find the user by email
    active_user = get_user_by_email(db, frompage.email_user)

    if not active_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get tasks for this user
    tasks = get_tasks_by_user(db, active_user.id)

    # Prepare the list of tasks with specifications
    task_with_spec_list = []
    for task in tasks:
        task_spec = get_task_spec_by_task_id(db, task.id)
        task_with_spec_list.append({
            "id": task.id,
            "title": task.title,
            "status_task": task.status_task,
            "description": task_spec.description if task_spec else None,
            "datetime_of_creation": task.datetime_of_creation,
        })

    return task_with_spec_list



