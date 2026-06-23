# Login application
# Database with user credentials
registration = {
    'user1': {"login_name": "pr", "password": "123"},
    'user2': {"login_name": "rj", "password": "rj123"},
    'user3': {"login_name": "ar", "password": "ar123"},
}

# Create a lookup dictionary for faster authentication
user_lookup = {user['login_name']: user['password'] for user in registration.values()}

def login(username: str, password: str):
    """Authenticate user by checking username and password."""
    if username in user_lookup:
        print("User found in the database")
        if password == user_lookup[username]:
            return {"status": True, "message": "Login successful"}
        else:
            return {"status": False, "message": "Login failed"}
    else:
        print("User not found in the database")

def main():
    """Get user input and perform login."""
    user_name = input("Please enter your username: ")
    password = input("Please enter your password: ")
    response = login(user_name, password)

    if response['status']:
        print (response['message'])
    else:
        print(response['message'])
main()







