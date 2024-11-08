from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from db.dependencies import get_db
from schemas import UserCreate, UserResponse, UserLogin
from db.crud import *
from db.db import init_db

from passlib.context import CryptContext
import bcrypt



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

    return {"message": "Login successful"}
