#!/usr/bin/env python3
"""
OpenHands SDK - Project Scaffolding Example

This example shows how to use OpenHands SDK to scaffold
complete projects with proper structure.
"""
import sys
sys.path.append('..')

from openhands_client import create_client

def main():
    print("=" * 60)
    print("OpenHands SDK - Project Scaffolding Example")
    print("=" * 60)
    
    with create_client(provider="deepseek_local") as client:
        
        # Example 1: Create a Python package
        print("\n📌 Example 1: Create a Python package")
        print("-" * 40)
        client.ask("""
Create a complete Python package called 'mypackage' with:

Structure:
mypackage/
├── mypackage/
│   ├── __init__.py
│   ├── core.py
│   ├── utils.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── pyproject.toml
├── README.md
├── LICENSE (MIT)
└── .gitignore

The package should:
- Have a simple Calculator class in core.py
- Have helper functions in utils.py
- Have a CLI interface using click
- Use pytest for testing
- Be installable with pip
""")
        
        # Example 2: Create a FastAPI project
        print("\n📌 Example 2: Create a FastAPI project")
        print("-" * 40)
        client.ask("""
Create a FastAPI project called 'fastapi_app' with:

Structure:
fastapi_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── users.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── database.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

Include:
- SQLAlchemy with SQLite
- Pydantic models
- CRUD operations
- JWT authentication stub
- Docker setup
""")
        
        # Example 3: Create a React + Vite project structure
        print("\n📌 Example 3: Create React project files")
        print("-" * 40)
        client.ask("""
Create the configuration files for a React + Vite + TypeScript project:

Create these files:
- package.json (with React 18, Vite, TypeScript, Tailwind CSS)
- vite.config.ts
- tsconfig.json
- tailwind.config.js
- postcss.config.js
- .eslintrc.cjs
- README.md with setup instructions

Put them in a folder called 'react_app'
""")
        
        # Show created structure
        print("\n📌 Created project structures:")
        print("-" * 40)
        result = client.run_command("find . -type f -name '*.py' -o -name '*.json' -o -name '*.toml' -o -name '*.md' | head -50")
        print(result)

    print("\n" + "=" * 60)
    print("✅ Project scaffolding completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
