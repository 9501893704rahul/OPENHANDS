#!/usr/bin/env python3
"""
OpenHands SDK - Basic Usage Example

This example shows how to use OpenHands SDK for basic operations:
- Running shell commands
- Reading and writing files
- Using the AI agent for tasks
"""
import sys
sys.path.append('..')

from openhands_client import create_client

def main():
    print("=" * 60)
    print("OpenHands SDK - Basic Usage Example")
    print("=" * 60)
    
    # Create client with DeepSeek local (via Ollama)
    # Make sure Ollama is running with DeepSeek model
    with create_client(provider="deepseek_local") as client:
        
        # Example 1: Run a shell command
        print("\n📌 Example 1: Running shell commands")
        print("-" * 40)
        result = client.run_command("echo 'Hello from OpenHands!' && date")
        print(f"Result: {result}")
        
        # Example 2: Write a file
        print("\n📌 Example 2: Writing a file")
        print("-" * 40)
        code = '''def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! Welcome to OpenHands."

if __name__ == "__main__":
    print(greet("Developer"))
'''
        client.write_file("hello.py", code)
        print("File 'hello.py' created!")
        
        # Example 3: Read the file back
        print("\n📌 Example 3: Reading a file")
        print("-" * 40)
        content = client.read_file("hello.py")
        print(f"File content:\n{content}")
        
        # Example 4: Run the Python file
        print("\n📌 Example 4: Running the Python file")
        print("-" * 40)
        output = client.run_command("python hello.py")
        print(f"Output: {output}")
        
        # Example 5: Ask AI to do a task
        print("\n📌 Example 5: AI-assisted task")
        print("-" * 40)
        print("Asking AI to create a utility function...")
        client.ask(
            "Create a Python file called 'utils.py' with a function that "
            "calculates the factorial of a number using recursion. "
            "Include docstrings and type hints."
        )
        
        # Read the created file
        utils_content = client.read_file("utils.py")
        print(f"Created utils.py:\n{utils_content}")

    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
