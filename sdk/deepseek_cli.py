#!/usr/bin/env python3
"""
DeepSeek CLI - Simple command-line interface for DeepSeek via Ollama

Usage:
    python deepseek_cli.py "Write a Python function to sort a list"
    python deepseek_cli.py --interactive
    python deepseek_cli.py --code "merge sort in Python"
    python deepseek_cli.py --review myfile.py
    python deepseek_cli.py --explain myfile.py
"""
import argparse
import sys

try:
    import ollama
except ImportError:
    print("Please install ollama: pip install ollama")
    sys.exit(1)

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner

console = Console()

DEFAULT_MODEL = "deepseek-coder-v2:16b"


def stream_response(prompt: str, model: str = DEFAULT_MODEL):
    """Stream response from DeepSeek."""
    console.print(f"\n[bold blue]🤖 DeepSeek ({model}):[/bold blue]\n")
    
    full_response = ""
    for chunk in ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    ):
        content = chunk["message"]["content"]
        full_response += content
        print(content, end="", flush=True)
    
    print("\n")
    return full_response


def chat(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Send prompt and get response."""
    with console.status("[bold green]Thinking...", spinner="dots"):
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
    return response["message"]["content"]


def generate_code(task: str, language: str = "python", model: str = DEFAULT_MODEL) -> str:
    """Generate code for a task."""
    prompt = f"""You are an expert {language} programmer. Generate clean, production-ready code.

Task: {task}

Requirements:
- Write only the code
- Include error handling
- Add type hints and docstrings
- Follow best practices

Code:"""
    
    return stream_response(prompt, model)


def review_file(filepath: str, model: str = DEFAULT_MODEL) -> str:
    """Review code in a file."""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        console.print(f"[red]File not found: {filepath}[/red]")
        return ""
    
    prompt = f"""Review this code and provide detailed feedback:

```
{code}
```

Check for:
1. Bugs and errors
2. Security vulnerabilities
3. Performance issues
4. Code style and best practices
5. Suggestions for improvement

Be specific and provide examples."""
    
    return stream_response(prompt, model)


def explain_file(filepath: str, model: str = DEFAULT_MODEL) -> str:
    """Explain code in a file."""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        console.print(f"[red]File not found: {filepath}[/red]")
        return ""
    
    prompt = f"""Explain this code in detail:

```
{code}
```

Provide:
1. Overview of what the code does
2. Step-by-step explanation
3. Key concepts used
4. Potential improvements"""
    
    return stream_response(prompt, model)


def fix_file(filepath: str, error: str = None, model: str = DEFAULT_MODEL) -> str:
    """Fix code in a file."""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        console.print(f"[red]File not found: {filepath}[/red]")
        return ""
    
    error_info = f"\nError: {error}" if error else ""
    
    prompt = f"""Fix this code:{error_info}

```
{code}
```

Provide the corrected code with comments explaining the fixes."""
    
    return stream_response(prompt, model)


def interactive_mode(model: str = DEFAULT_MODEL):
    """Run interactive chat mode."""
    console.print(Panel.fit(
        f"[bold blue]DeepSeek Interactive Mode[/bold blue]\n"
        f"Model: {model}\n"
        f"Commands: /code, /review <file>, /explain <file>, /fix <file>, /quit",
        title="🧠 DeepSeek CLI"
    ))
    
    history = []
    
    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""
                
                if cmd in ["/quit", "/exit", "/q"]:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                elif cmd == "/code":
                    if arg:
                        generate_code(arg, model=model)
                    else:
                        console.print("[yellow]Usage: /code <task description>[/yellow]")
                elif cmd == "/review":
                    if arg:
                        review_file(arg, model=model)
                    else:
                        console.print("[yellow]Usage: /review <filepath>[/yellow]")
                elif cmd == "/explain":
                    if arg:
                        explain_file(arg, model=model)
                    else:
                        console.print("[yellow]Usage: /explain <filepath>[/yellow]")
                elif cmd == "/fix":
                    if arg:
                        fix_file(arg, model=model)
                    else:
                        console.print("[yellow]Usage: /fix <filepath>[/yellow]")
                elif cmd == "/clear":
                    history = []
                    console.print("[yellow]History cleared[/yellow]")
                elif cmd == "/help":
                    console.print("""
[bold]Available commands:[/bold]
  /code <task>     - Generate code for a task
  /review <file>   - Review code in a file
  /explain <file>  - Explain code in a file
  /fix <file>      - Fix code in a file
  /clear           - Clear conversation history
  /quit            - Exit
""")
                else:
                    console.print(f"[yellow]Unknown command: {cmd}[/yellow]")
                continue
            
            # Regular chat
            history.append({"role": "user", "content": user_input})
            
            console.print(f"\n[bold blue]🤖 DeepSeek:[/bold blue]")
            
            full_response = ""
            for chunk in ollama.chat(
                model=model,
                messages=history,
                stream=True
            ):
                content = chunk["message"]["content"]
                full_response += content
                print(content, end="", flush=True)
            
            print()
            history.append({"role": "assistant", "content": full_response})
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use /quit to exit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def list_models():
    """List available Ollama models."""
    try:
        models = ollama.list()
        console.print("\n[bold]Available Models:[/bold]\n")
        for model in models.get("models", []):
            name = model.get("name", "unknown")
            size = model.get("size", 0) / (1024**3)  # Convert to GB
            console.print(f"  • {name} ({size:.1f} GB)")
    except Exception as e:
        console.print(f"[red]Error listing models: {e}[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="DeepSeek CLI - AI coding assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Write a Python quicksort function"
  %(prog)s --interactive
  %(prog)s --code "REST API with FastAPI"
  %(prog)s --review myfile.py
  %(prog)s --explain myfile.py
  %(prog)s --fix myfile.py --error "IndexError"
        """
    )
    
    parser.add_argument("prompt", nargs="?", help="Prompt to send to DeepSeek")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive chat mode")
    parser.add_argument("-c", "--code", metavar="TASK", help="Generate code for a task")
    parser.add_argument("-r", "--review", metavar="FILE", help="Review code in a file")
    parser.add_argument("-e", "--explain", metavar="FILE", help="Explain code in a file")
    parser.add_argument("-f", "--fix", metavar="FILE", help="Fix code in a file")
    parser.add_argument("--error", help="Error message (for --fix)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("-l", "--list", action="store_true", help="List available models")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming output")
    
    args = parser.parse_args()
    
    # List models
    if args.list:
        list_models()
        return
    
    # Interactive mode
    if args.interactive:
        interactive_mode(args.model)
        return
    
    # Code generation
    if args.code:
        generate_code(args.code, model=args.model)
        return
    
    # Review file
    if args.review:
        review_file(args.review, model=args.model)
        return
    
    # Explain file
    if args.explain:
        explain_file(args.explain, model=args.model)
        return
    
    # Fix file
    if args.fix:
        fix_file(args.fix, args.error, model=args.model)
        return
    
    # Direct prompt
    if args.prompt:
        if args.no_stream:
            response = chat(args.prompt, args.model)
            console.print(Markdown(response))
        else:
            stream_response(args.prompt, args.model)
        return
    
    # No arguments - show help
    parser.print_help()


if __name__ == "__main__":
    main()
