# OpenHands Python SDK

Use OpenHands programmatically with Python for AI-powered coding assistance.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install OpenHands SDK directly
pip install openhands-ai ollama python-dotenv rich
```

### Prerequisites

1. **Ollama running with DeepSeek** (for local LLM):
```bash
# Start Ollama (if using Docker)
docker run -d --gpus all -p 11434:11434 -v ollama:/root/.ollama ollama/ollama

# Pull DeepSeek model
docker exec -it ollama ollama pull deepseek-coder-v2:16b
```

2. **Or use cloud LLM** (OpenAI, Anthropic, DeepSeek API):
```bash
# Set environment variables
export OPENAI_API_KEY="your-key"
# or
export ANTHROPIC_API_KEY="your-key"
# or
export DEEPSEEK_API_KEY="your-key"
```

### Basic Usage

```python
from openhands_client import create_client

# Using DeepSeek locally via Ollama
with create_client(provider="deepseek_local") as client:
    # Run shell commands
    result = client.run_command("ls -la")
    print(result)
    
    # Write files
    client.write_file("hello.py", "print('Hello World!')")
    
    # Read files
    content = client.read_file("hello.py")
    
    # Ask AI to do tasks
    client.ask("Create a Python function that sorts a list using quicksort")
    
    # Browse web pages
    page = client.browse_url("https://example.com")
    print(page["content"])
```

### Async Usage

```python
import asyncio
from openhands_client import OpenHandsClient

async def main():
    client = OpenHandsClient(provider="deepseek_local")
    await client.start()
    
    # Run commands concurrently
    results = await asyncio.gather(
        client.run_command("echo 'Task 1'"),
        client.run_command("echo 'Task 2'"),
        client.run_command("echo 'Task 3'"),
    )
    
    await client.stop()

asyncio.run(main())
```

## 📁 Project Structure

```
sdk/
├── config.py              # Configuration management
├── openhands_client.py    # Main SDK client
├── requirements.txt       # Dependencies
├── README.md             # This file
└── examples/
    ├── 01_basic_usage.py         # Basic operations
    ├── 02_code_generation.py     # AI code generation
    ├── 03_browser_automation.py  # Web browsing
    ├── 04_project_scaffolding.py # Create project structures
    ├── 05_async_usage.py         # Async/concurrent operations
    └── 06_deepseek_direct.py     # Direct Ollama/DeepSeek usage
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# LLM Provider (deepseek_local, deepseek_api, openai, anthropic)
LLM_PROVIDER=deepseek_local

# API Keys (for cloud providers)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEEPSEEK_API_KEY=sk-...

# Workspace directory
WORKSPACE_DIR=./workspace

# OpenHands server URL (if using remote)
OPENHANDS_SERVER_URL=http://localhost:3000
```

### Available Providers

| Provider | Model | Description |
|----------|-------|-------------|
| `deepseek_local` | `ollama/deepseek-coder-v2:16b` | Local GPU via Ollama |
| `deepseek_api` | `deepseek-chat` | DeepSeek cloud API |
| `openai` | `gpt-4o` | OpenAI API |
| `anthropic` | `claude-sonnet-4-20250514` | Anthropic API |

## 📚 API Reference

### OpenHandsClient

```python
class OpenHandsClient:
    def __init__(
        self,
        provider: str = "deepseek_local",  # LLM provider
        workspace_dir: str = None,          # Working directory
        verbose: bool = True                # Print output
    )
```

### Methods

#### `run_command(command: str) -> str`
Execute a shell command and return output.

```python
result = client.run_command("python --version")
```

#### `read_file(filepath: str) -> str`
Read file contents from workspace.

```python
content = client.read_file("src/main.py")
```

#### `write_file(filepath: str, content: str) -> bool`
Write content to a file.

```python
client.write_file("output.txt", "Hello World")
```

#### `browse_url(url: str) -> Dict`
Browse a URL and get page content.

```python
page = client.browse_url("https://example.com")
print(page["content"])
print(page["screenshot"])  # Base64 screenshot
```

#### `ask(task: str, max_iterations: int = 10) -> State`
Ask the AI agent to complete a task.

```python
state = client.ask("Create a REST API with FastAPI")
```

#### `code_task(task: str, language: str, filename: str) -> str`
Generate code for a specific task.

```python
code = client.code_task(
    task="sort a list using merge sort",
    language="python",
    filename="sort.py"
)
```

## 🎯 Examples

### 1. Generate a Complete Project

```python
with create_client() as client:
    client.ask("""
    Create a complete Flask blog application with:
    - User authentication
    - CRUD for blog posts
    - SQLite database
    - Bootstrap templates
    - Requirements.txt
    - README with setup instructions
    """)
```

### 2. Code Review

```python
with create_client() as client:
    code = client.read_file("my_code.py")
    client.ask(f"""
    Review this code and suggest improvements:
    
    ```python
    {code}
    ```
    
    Check for:
    - Bugs
    - Security issues
    - Performance
    - Best practices
    """)
```

### 3. Automated Testing

```python
with create_client() as client:
    # Generate tests
    client.ask("Write pytest tests for all functions in src/utils.py")
    
    # Run tests
    result = client.run_command("pytest tests/ -v")
    print(result)
```

### 4. Web Scraping

```python
with create_client() as client:
    client.ask("""
    Browse to https://news.ycombinator.com
    Extract the top 10 stories with titles, points, and links
    Save to hacker_news.json
    """)
```

### 5. Direct DeepSeek Usage (Lightweight)

```python
import ollama

# Simple chat
response = ollama.chat(
    model="deepseek-coder-v2:16b",
    messages=[{"role": "user", "content": "Write a Python quicksort"}]
)
print(response["message"]["content"])

# Streaming
for chunk in ollama.chat(
    model="deepseek-coder-v2:16b",
    messages=[{"role": "user", "content": "Explain recursion"}],
    stream=True
):
    print(chunk["message"]["content"], end="")
```

## 🐛 Troubleshooting

### Ollama Connection Error
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
docker restart ollama
```

### Model Not Found
```bash
# List available models
ollama list

# Pull the model
ollama pull deepseek-coder-v2:16b
```

### Out of Memory
```bash
# Use a smaller model
ollama pull deepseek-coder:6.7b

# Update config.py to use smaller model
```

### Import Errors
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install openhands-ai ollama python-dotenv rich
```

## 🔗 Links

- [OpenHands Documentation](https://docs.all-hands.dev/)
- [OpenHands GitHub](https://github.com/All-Hands-AI/OpenHands)
- [Ollama](https://ollama.ai/)
- [DeepSeek](https://www.deepseek.com/)
