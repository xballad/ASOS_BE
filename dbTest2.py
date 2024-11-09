from db.db import SessionLocal, engine
import db.user
import db.team
import db.task
import db.task_spec

from db.crud import *

# Run tests

# Creating table
db.user.Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Create users and teams
user1 = create_user(db, "John", "Doe", "johndoe2", "password", "johndoe2@example.com", "salt")
team1 = create_team(db, "Team A")

# Create tasks
task1 = create_task(db, "Task 1", "in_progress", user_id=user1.id)
task2 = create_task(db, "Task 2", "completed", team_id=team1.id)

# Get tasks by user
tasks_for_user = get_tasks_by_user(db, user1.id)
print(f"Tasks for user {user1.username}: {tasks_for_user}")

# Get tasks by team
tasks_for_team = get_tasks_by_team(db, team1.id)
print(f"Tasks for team {team1.name}: {tasks_for_team}")

# Get task by ID
task_by_id = get_task_by_id(db, task1.id)
print(f"Task with ID {task1.id}: {task_by_id}")

add_user_to_team(db, user1.id, team1.id)



