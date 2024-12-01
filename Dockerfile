# Step 1: Use an official Python image as a base
FROM python:3.11-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy the requirements.txt (make sure it's in your project folder)
COPY requirements.txt .

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your FastAPI app into the container
COPY . .

# Step 6: Expose the port FastAPI app will run on
EXPOSE 8000

# Step 8: Start FastAPI with Uvicorn (with SSL support)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "/app/keys/selfsigned.key", "--ssl-certfile", "/app/keys/selfsigned.crt"]
