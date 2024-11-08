
from db import SessionLocal, engine
import user
from db.crud import create_user, get_users, update_user_name, update_user_last_name, update_user_email, \
    update_user_username, update_user_password, delete_user, get_user_by_id

# Run tests

# Creating table
user.Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Create a new user
new_user = create_user(db, name="John", last_name="Doe", username="johndoe3", password="password123",
                       email="john.doe3@example.com")
print(f"Created User: {new_user}")

# Get the user by ID
user_by_id = get_user_by_id(db, new_user.id)
print(f"User by ID: {user_by_id}")

# Update the user's name
updated_user_name = update_user_name(db, new_user.id, name="John Updated")
print(f"Updated Name: {updated_user_name}")

# Update the user's last name
updated_user_last_name = update_user_last_name(db, new_user.id, last_name="Doe Updated")
print(f"Updated Last Name: {updated_user_last_name}")

# Get all users
all_users = get_users(db)
print(f"All Users: {all_users}")

# Delete the user
deleted_user = delete_user(db, new_user.id)
print(f"Deleted User: {deleted_user}")

