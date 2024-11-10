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

user1 = create_user(db, name="John", last_name="Doe", username="johndoe", password="password123",
                    email="john@example.com", salt="somesalt")
user2 = create_user(db, name="Jane", last_name="Smith", username="janesmith", password="password456",
                    email="jane@example.com", salt="othersalt")

assert user1.id is not None
assert user2.id is not None

# Step 2: Fetch Users
users = get_users(db)
assert len(users) >= 2

# Step 3: Update User
updated_user = update_user_name(db, user1.id, "Johnny")
assert updated_user.name == "Johnny"

# Step 4: Delete User
# deleted_user = delete_user(db, user2.id)
# assert deleted_user is not None
# assert get_user_by_id(db, user2.id) is None

# Step 5: Create Team
team1 = create_team(db, name="Developers")
team2 = create_team(db, name="Designers")

assert team1.id is not None
assert team2.id is not None

# Step 6: Update Team
updated_team = update_team_name(db, team1.id, "Backend Developers")
assert updated_team.name == "Backend Developers"

# Step 7: Delete Team
# deleted_team = delete_team(db, team2.id)
# assert deleted_team is not None
# assert get_team_by_id(db, team2.id) is None

# Step 8: Add User to Team
team_with_user = add_user_to_team(db, user1.id, team1.id)
add_user_to_team(db, user2.id, team1.id)
add_user_to_team(db, user1.id, team2.id)
assert team_with_user is not None
# assert len(get_users_in_team(db, team1.id)) == 1

# Step 9: Remove User from Team
# team_after_removal = remove_user_from_team(db, user1.id, team1.id)
# assert team_after_removal is not None
# assert len(get_users_in_team(db, team1.id)) == 0

# Step 10: Create Task
task1 = create_task(db, title="Build API", status_task="in progress", user_id=user1.id)
task2 = create_task(db, title="Design UI", status_task="pending", team_id=team1.id)

assert task1.id is not None
assert task2.id is not None

# Step 11: Get Task by ID and Owner
fetched_task_by_id = get_task_by_id(db, task1.id)
assert fetched_task_by_id.title == "Build API"

user_tasks = get_tasks_by_user(db, user1.id)
assert len(user_tasks) == 1

team_tasks = get_tasks_by_team(db, team1.id)
assert len(team_tasks) == 1

# Step 12: Delete Task
# deleted_task = delete_task(db, task2.id)
# assert deleted_task is not None
# assert get_task_by_id(db, task2.id) is None

# Step 13: Create TaskSpec
task_spec1 = create_task_spec(db, task_id=task1.id, description="Build a RESTful API")
assert task_spec1.id is not None

# Step 14: Update TaskSpec
updated_task_spec = update_task_spec(db, task_spec1.id, description="Build a GraphQL API")
assert updated_task_spec.description == "Build a GraphQL API"

# Step 15: Delete TaskSpec
# deleted_task_spec = delete_task_spec(db, task_spec1.id)
# assert deleted_task_spec is not None
# assert get_task_spec_by_id(db, task_spec1.id) is None

# Step 16: Create Comment
comment1 = create_comment(db, text="Great progress!", task_spec_id=task1.id, user_username="johndoe")
comment2 = create_comment(db, text="Needs revision", task_spec_id=task1.id, user_username="johndoe")
assert comment1.id is not None
assert comment2.id is not None

# Step 17: Get Comments by Username and TaskSpec
user_comments = get_comments_by_username(db, "johndoe")
assert len(user_comments) >= 2

# Step 18: Update Comment
updated_comment = update_comment_text(db, comment1.id, "Excellent progress!")
assert updated_comment.text == "Excellent progress!"

# Step 19: Delete Comment
# deleted_comment = delete_comment(db, comment1.id)
# assert deleted_comment is not None
# assert get_comment_by_id(db, comment1.id) is None
print(get_comments_by_username(db, username=user1.username))
print(get_users_in_team(db,team1.id))


print("All tests passed successfully!")
