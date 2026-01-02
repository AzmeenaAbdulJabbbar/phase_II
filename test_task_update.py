import requests
import json

# Test updating a task to verify the timezone issue is fixed
def test_update_task():
    base_url = "http://127.0.0.1:8000"
    
    # First, register a user
    signup_url = f"{base_url}/api/auth/signup"
    signup_data = {
        "email": "test3@example.com",
        "password": "password123",
        "name": "Test User 3"
    }
    
    print("Registering a user...")
    try:
        signup_response = requests.post(signup_url, json=signup_data)
        print(f"Signup Status Code: {signup_response.status_code}")
        
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
                    "title": "Test task for update",
                    "description": "This is a test task to verify update works"
                }
                
                create_response = requests.post(tasks_url, headers=headers, json=task_data)
                print(f"Task Creation Status Code: {create_response.status_code}")
                
                if create_response.status_code == 201:
                    created_task = create_response.json()
                    task_id = created_task.get("data", {}).get("id")
                    print(f"Task created successfully with ID: {task_id}")
                    
                    # Now try to update the created task (toggle completion)
                    print(f"Updating task with ID: {task_id}")
                    update_task_url = f"{base_url}/api/tasks/{task_id}"
                    update_data = {
                        "completed": True
                    }
                    update_response = requests.patch(update_task_url, headers=headers, json=update_data)
                    print(f"Update Task Status Code: {update_response.status_code}")
                    print(f"Update Task Response: {update_response.text}")
                    
                    if update_response.status_code == 200:
                        print("SUCCESS: Task update works! The timezone issue has been fixed.")
                    else:
                        print("FAILED: Task update failed.")
                        
                    # Also try to get all tasks
                    print("Getting all tasks for the user...")
                    all_tasks_response = requests.get(tasks_url, headers=headers)
                    print(f"Get All Tasks Status Code: {all_tasks_response.status_code}")
                    print(f"Get All Tasks Response: {all_tasks_response.text}")
                else:
                    print("FAILED: Task creation failed.")
            else:
                print("FAILED: No token received from signup.")
        else:
            print("FAILED: User registration failed.")
            
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    print("Testing task update after timezone fix...")
    test_update_task()