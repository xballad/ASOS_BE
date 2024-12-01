from locust import HttpUser, task, between
import uuid

class FastAPIUser(HttpUser):
    # Time between the execution of tasks (in seconds)
    wait_time = between(1, 5)

    def on_start(self):
        """Executed when a virtual user starts running."""
        # Generate a unique email address for each virtual user using UUID
        self.user_id = uuid.uuid4().hex[:8]  # Use the first 8 characters of the UUID
        self.email = f"testuser{self.user_id}@example.com"
        self.username = f"testuser_{self.user_id}"

    @task(1)
    def register_user(self):
        """Test user registration."""
        user_data = {
            "name": "John",
            "last_name": "Doe",
            "username": self.username,
            "password": "password123",
            "email": self.email
        }
        response = self.client.post("/api/register", json=user_data)
        assert response.status_code == 200
        print(f"User {user_data['email']} registered")

    @task(2)
    def login_user(self):
        """Test user login."""
        login_data = {
            "email": self.email,
            "password": "password123"
        }
        response = self.client.post("/api/login", json=login_data)
        assert response.status_code == 200
        self.token = response.json().get("access_token")
        print(f"User {login_data['email']} logged in")

    @task(3)
    def create_task(self):
        """Test task creation."""
        if hasattr(self, 'token'):
            task_data = {
                "title": "Test Task",
                "status_task": "pending",
                "description": "This is a test task.",
                "email_creator": self.email,
                "email_assigned": self.email,
                "team_assigned": 1
            }
            response = self.client.post(
                "/api/create/task",
                json=task_data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            assert response.status_code == 200
            print(f"Task created: {task_data['title']}")
        else:
            print("User not logged in yet, skipping task creation.")

    @task(4)
    def get_dashboard(self):
        """Test accessing the dashboard."""
        if hasattr(self, 'token'):
            response = self.client.get(
                "/api/dashboard",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            assert response.status_code == 200
            print("Dashboard accessed.")
        else:
            print("User not logged in yet, skipping dashboard access.")
