import string

from typing import List
from urllib.request import Request

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.testing.pickleable import EmailUser
from starlette.responses import RedirectResponse

from db.dependencies import get_db
from jwtS.workToken import create_access_token, verify_token
from schemas import *
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
    allow_origins=["*"],  # Allows Angular app to access backend
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

@app.middleware("http")
async def enforce_https(request: Request, call_next):
    if request.url.scheme != "https":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url=str(url))
    response = await call_next(request)
    return response


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

@app.post("/api/user/changepassword", tags=["User Change Password"], summary="Change password")
async def changing_password(frompage: GetChangeForm, db: Session = Depends(get_db)):
    print(frompage)
    db_user = get_user_by_email(db, frompage.emailUser)

    if not db_user:
        raise HTTPException(status_code=406, detail="User not found")


    salt = db_user.salt.encode('utf-8')
    stored_hashed_password = db_user.password.encode('utf-8')
    provided_hashed_password = bcrypt.hashpw(frompage.oldPassword.encode('utf-8'), salt)

    if provided_hashed_password != stored_hashed_password:
        raise HTTPException(status_code=401, detail="Old password is inccorect")

    new_password = bcrypt.hashpw(frompage.newPassword.encode('utf-8'), salt)
    update_user_password(db = db,
                         user_id=db_user.id,
                         password= new_password.decode('utf-8'))

    return {"message": "Password has been changed successfully."}


@app.post("/api/create-team", tags=["Create team"], summary="Create a new team")
async def creation_of_team(frompage: CreationTeamForm, db: Session = Depends(get_db)):
    # creation of team
    team_name = frompage.teamName
    created_team = create_team(db=db,name=team_name)

    #working with potentional members
    members = frompage.members
    existing_members = []
    non_existing_members = []

    for email in members:
        user = get_user_by_email(db, email)
        if user:
            existing_members.append(user.id)
            add_user_to_team(db=db,user_id=user.id,team_id=created_team.id)
        else:
            non_existing_members.append(email)

    if non_existing_members:
        raise HTTPException(
            status_code=404,
            detail=f"These members do not exist: {', '.join(non_existing_members)}"
        )

    return "Team has been created successfully."

@app.post("/api/getTeamsForMembers", tags=["Teams"], summary="Get teams for a user")
async def get_teams_for_user_endpoint(emailuser: GetListOfTasksForUser, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db,emailuser.email_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    teams = get_teams_for_user(db = db,user_id=db_user.id)
    if teams is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found for the user")
    return teams


@app.get("/api/teams/members/{team_id}")
async def get_team_members(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return [{"id": user.id, "email": user.email} for user in team.users]

@app.put("/api/teams/update/members")
async def update_team(frompage: UpdateTeamFrom, db: Session = Depends(get_db)):
    team_id = frompage.team_id
    new_member_emails = frompage.members  # This will be the updated list of member emails

    db_team = get_team_by_id(db=db,team_id=team_id)

    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Handle team name change
    if frompage.team_name != db_team.name:
        update_team_name(db=db,team_id=team_id,name=frompage.team_name)

    current_members =  get_users_in_team(db=db,team_id=team_id)

    current_member_emails = [user.email for user in current_members]

    for email in new_member_emails:
        if email not in current_member_emails:
            db_user = get_user_by_email(db=db, email=email)
            if db_user:
                add_user_to_team(db=db,user_id=db_user.id,team_id=team_id)
            else:
                raise HTTPException(status_code=404, detail=f"User {email} not found")

    # Check for removed members
    for email in current_member_emails:
        if email not in new_member_emails:
            db_user = get_user_by_email(db=db, email=email)
            if db_user:
                remove_user_from_team(db=db,user_id=db_user.id,team_id=team_id)

    return {"message": "Team updated successfully", "team": db_team}


@app.put("/api/task/update")
def task_status_update(task_info: UpdateTask, db: Session = Depends(get_db)):
    db_task = get_task_by_id(db=db,task_id=task_info.task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_task_status(db=db,task_id=task_info.task_id, new_status=task_info.status)
    return {"message": "Task updated successfully"}