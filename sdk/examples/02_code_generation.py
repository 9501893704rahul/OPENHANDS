#!/usr/bin/env python3
"""
OpenHands SDK - Code Generation Example

This example shows how to use OpenHands SDK to generate code
for various programming tasks using DeepSeek or other LLMs.
"""
import sys
sys.path.append('..')

from openhands_client import create_client

def main():
    print("=" * 60)
    print("OpenHands SDK - Code Generation Example")
    print("=" * 60)
    
    with create_client(provider="deepseek_local") as client:
        
        # Example 1: Generate a Python class
        print("\n📌 Example 1: Generate a Python class")
        print("-" * 40)
        client.ask("""
Create a Python file called 'models/user.py' with a User class that has:
- Attributes: id, username, email, created_at
- Methods: to_dict(), from_dict(), validate_email()
- Use dataclasses
- Include type hints and docstrings
""")
        
        # Example 2: Generate a REST API endpoint
        print("\n📌 Example 2: Generate a FastAPI endpoint")
        print("-" * 40)
        client.ask("""
Create a file called 'api/routes.py' with FastAPI routes for:
- GET /users - list all users
- GET /users/{id} - get user by id
- POST /users - create new user
- PUT /users/{id} - update user
- DELETE /users/{id} - delete user

Include proper error handling and response models.
""")
        
        # Example 3: Generate unit tests
        print("\n📌 Example 3: Generate unit tests")
        print("-" * 40)
        client.ask("""
Create a file called 'tests/test_user.py' with pytest tests for the User class.
Include tests for:
- Creating a user
- Converting to/from dict
- Email validation
- Edge cases
""")
        
        # Example 4: Generate a CLI tool
        print("\n📌 Example 4: Generate a CLI tool")
        print("-" * 40)
        client.ask("""
Create a file called 'cli.py' with a command-line tool using argparse that:
- Has subcommands: list, add, remove, update
- Works with a JSON file for storage
- Has colored output using rich library
- Includes help text for all commands
""")
        
        # List all generated files
        print("\n📌 Generated files:")
        print("-" * 40)
        result = client.run_command("find . -name '*.py' -type f")
        print(result)

    print("\n" + "=" * 60)
    print("✅ Code generation completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
