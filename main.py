from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from db.dependencies import get_db
from schemas import UserCreate, UserResponse
from db.crud import create_user, get_user_by_email
from db.db import init_db


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


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/register", response_model=UserResponse, tags=["User Registration"], summary="Register a new user")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email or username is already taken
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email is already in use")

    # Create the user
    db_user = create_user(db, name=user.name, last_name=user.last_name, username=user.username, password=user.password,
                          email=user.email)

    return db_user  # Returns UserResponse schema
