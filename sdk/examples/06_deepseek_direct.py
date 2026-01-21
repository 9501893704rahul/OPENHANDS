#!/usr/bin/env python3
"""
OpenHands SDK - Direct DeepSeek/Ollama Usage

This example shows how to use DeepSeek directly via Ollama
without the full OpenHands runtime (lighter weight).
"""
import sys
sys.path.append('..')

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("Install ollama: pip install ollama")

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def chat_with_deepseek(prompt: str, model: str = "deepseek-coder-v2:16b") -> str:
    """
    Send a prompt to DeepSeek via Ollama and get response.
    
    Args:
        prompt: The prompt to send
        model: Ollama model name
        
    Returns:
        Model response
    """
    if not OLLAMA_AVAILABLE:
        return "Ollama not installed"
    
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


def generate_code(task: str, language: str = "python") -> str:
    """
    Generate code for a specific task.
    
    Args:
        task: Description of what the code should do
        language: Programming language
        
    Returns:
        Generated code
    """
    prompt = f"""You are an expert {language} programmer. Write clean, production-ready code.

Task: {task}

Requirements:
- Write only the code, no explanations
- Include proper error handling
- Add type hints (if applicable)
- Add brief docstrings

Output only the code:"""
    
    return chat_with_deepseek(prompt)


def explain_code(code: str) -> str:
    """
    Get an explanation of code.
    
    Args:
        code: The code to explain
        
    Returns:
        Explanation
    """
    prompt = f"""Explain this code in detail:

```
{code}
```

Provide:
1. What the code does
2. How it works step by step
3. Any potential issues or improvements"""
    
    return chat_with_deepseek(prompt)


def review_code(code: str) -> str:
    """
    Get a code review.
    
    Args:
        code: The code to review
        
    Returns:
        Code review
    """
    prompt = f"""Review this code and provide feedback:

```
{code}
```

Check for:
1. Bugs or errors
2. Security issues
3. Performance problems
4. Code style and best practices
5. Suggestions for improvement

Be specific and provide examples."""
    
    return chat_with_deepseek(prompt)


def fix_code(code: str, error: str = None) -> str:
    """
    Fix buggy code.
    
    Args:
        code: The buggy code
        error: Optional error message
        
    Returns:
        Fixed code
    """
    error_info = f"\nError message: {error}" if error else ""
    
    prompt = f"""Fix this code:{error_info}

```
{code}
```

Provide only the corrected code with brief comments explaining the fixes."""
    
    return chat_with_deepseek(prompt)


def main():
    console.print(Panel.fit(
        "[bold blue]OpenHands SDK - Direct DeepSeek Usage[/bold blue]\n"
        "Using DeepSeek via Ollama for lightweight AI coding assistance",
        title="🧠 DeepSeek Direct"
    ))
    
    if not OLLAMA_AVAILABLE:
        console.print("[red]Please install ollama: pip install ollama[/red]")
        return
    
    # Example 1: Generate code
    console.print("\n[bold cyan]📌 Example 1: Generate Code[/bold cyan]")
    console.print("-" * 50)
    
    code = generate_code("a function that validates email addresses using regex")
    console.print(Markdown(f"```python\n{code}\n```"))
    
    # Example 2: Explain code
    console.print("\n[bold cyan]📌 Example 2: Explain Code[/bold cyan]")
    console.print("-" * 50)
    
    sample_code = '''
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
'''
    
    explanation = explain_code(sample_code)
    console.print(Markdown(explanation))
    
    # Example 3: Code review
    console.print("\n[bold cyan]📌 Example 3: Code Review[/bold cyan]")
    console.print("-" * 50)
    
    code_to_review = '''
def get_user(id):
    query = f"SELECT * FROM users WHERE id = {id}"
    result = db.execute(query)
    return result
'''
    
    review = review_code(code_to_review)
    console.print(Markdown(review))
    
    # Example 4: Fix code
    console.print("\n[bold cyan]📌 Example 4: Fix Code[/bold cyan]")
    console.print("-" * 50)
    
    buggy_code = '''
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 0)
print(result)
'''
    
    fixed = fix_code(buggy_code, "ZeroDivisionError: division by zero")
    console.print(Markdown(f"```python\n{fixed}\n```"))
    
    # Interactive mode
    console.print("\n[bold green]💬 Interactive Mode[/bold green]")
    console.print("Type your coding questions (or 'quit' to exit)")
    console.print("-" * 50)
    
    while True:
        try:
            user_input = input("\n🤖 You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            if not user_input:
                continue
            
            response = chat_with_deepseek(user_input)
            console.print("\n[bold blue]DeepSeek:[/bold blue]")
            console.print(Markdown(response))
            
        except KeyboardInterrupt:
            break
    
    console.print("\n[bold green]✅ Done![/bold green]")


if __name__ == "__main__":
    main()
