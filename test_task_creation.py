import requests
import json

# Test creating a task to verify the due_date column issue is fixed
def test_create_task():
    base_url = "http://127.0.0.1:8000"

    # First, register a user
    signup_url = f"{base_url}/api/auth/signup"
    signup_data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    print("Registering a user...")
    try:
        signup_response = requests.post(signup_url, json=signup_data)
        print(f"Signup Status Code: {signup_response.status_code}")
        print(f"Signup Response: {signup_response.text}")

        if signup_response.status_code == 200:
            response_data = signup_response.json()
            token = response_data.get("data", {}).get("token")

            if token:
                print("User registered successfully, now creating a task...")

                # Create a task with the authentication token
                tasks_url = f"{base_url}/api/tasks/"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                    "Origin": "http://localhost:3000"
                }

                # Sample task data
                task_data = {
                    "title": "Test task after fix",
                    "description": "This is a test to verify the due_date column fix"
                }

                response = requests.post(tasks_url, headers=headers, json=task_data)
                print(f"Task Creation Status Code: {response.status_code}")
                print(f"Task Creation Response: {response.text}")

                if response.status_code == 201:
                    print("SUCCESS: Task created successfully! The due_date column issue has been fixed.")
                else:
                    print("FAILED: Task creation failed.")
            else:
                print("FAILED: No token received from signup.")
        else:
            print("FAILED: User registration failed.")

    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    print("Testing task creation after due_date column fix...")
    test_create_task()