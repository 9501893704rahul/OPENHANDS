"""
OpenHands SDK Client - Main interface for programmatic control
"""
import asyncio
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

try:
    from openhands.core.config import AppConfig, LLMConfig, SandboxConfig
    from openhands.core.main import create_runtime, run_controller
    from openhands.controller.state.state import State
    from openhands.events.action import (
        CmdRunAction,
        FileWriteAction,
        FileReadAction,
        BrowseURLAction,
        MessageAction,
    )
    from openhands.events.observation import (
        CmdOutputObservation,
        FileReadObservation,
        FileWriteObservation,
        BrowserOutputObservation,
    )
    OPENHANDS_AVAILABLE = True
except ImportError:
    OPENHANDS_AVAILABLE = False
    print("⚠️  OpenHands SDK not installed. Install with: pip install openhands-ai")

from config import get_llm_config, WORKSPACE_DIR

console = Console()


class OpenHandsClient:
    """
    OpenHands SDK Client for programmatic AI coding assistance.
    
    Features:
    - Execute shell commands
    - Read/write files
    - Browse web pages
    - Run full coding agents
    - Integrate with DeepSeek, OpenAI, Anthropic, etc.
    """
    
    def __init__(
        self,
        provider: str = "deepseek_local",
        workspace_dir: str = None,
        verbose: bool = True
    ):
        """
        Initialize OpenHands client.
        
        Args:
            provider: LLM provider (deepseek_local, deepseek_api, openai, anthropic)
            workspace_dir: Directory for file operations
            verbose: Print detailed output
        """
        if not OPENHANDS_AVAILABLE:
            raise ImportError("OpenHands SDK not installed. Run: pip install openhands-ai")
        
        self.provider = provider
        self.workspace_dir = Path(workspace_dir or WORKSPACE_DIR).resolve()
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        
        # Get LLM configuration
        llm_config = get_llm_config(provider)
        
        # Initialize OpenHands config
        self.config = AppConfig(
            llm=LLMConfig(
                model=llm_config["model"],
                api_key=llm_config["api_key"],
                base_url=llm_config["base_url"],
            ),
            sandbox=SandboxConfig(
                base_container_image="docker.all-hands.dev/all-hands-ai/runtime:main",
            ),
            workspace_base=str(self.workspace_dir),
        )
        
        self.runtime = None
        self._log(f"✅ OpenHands client initialized with {provider}")
        self._log(f"📁 Workspace: {self.workspace_dir}")
    
    def _log(self, message: str):
        """Print message if verbose mode is enabled."""
        if self.verbose:
            console.print(message)
    
    async def start(self):
        """Start the OpenHands runtime."""
        self._log("🚀 Starting OpenHands runtime...")
        self.runtime = await create_runtime(self.config)
        self._log("✅ Runtime started")
        return self
    
    async def stop(self):
        """Stop the OpenHands runtime."""
        if self.runtime:
            await self.runtime.close()
            self._log("🛑 Runtime stopped")
    
    async def run_command(self, command: str) -> str:
        """
        Execute a shell command.
        
        Args:
            command: Shell command to execute
            
        Returns:
            Command output
        """
        self._log(f"💻 Running: {command}")
        action = CmdRunAction(command=command)
        observation = await self.runtime.run_action(action)
        
        if isinstance(observation, CmdOutputObservation):
            output = observation.content
            self._log(f"📤 Output:\n{output}")
            return output
        return str(observation)
    
    async def read_file(self, filepath: str) -> str:
        """
        Read a file from the workspace.
        
        Args:
            filepath: Path to file (relative to workspace)
            
        Returns:
            File contents
        """
        full_path = self.workspace_dir / filepath
        self._log(f"📖 Reading: {full_path}")
        
        action = FileReadAction(path=str(full_path))
        observation = await self.runtime.run_action(action)
        
        if isinstance(observation, FileReadObservation):
            return observation.content
        return str(observation)
    
    async def write_file(self, filepath: str, content: str) -> bool:
        """
        Write content to a file.
        
        Args:
            filepath: Path to file (relative to workspace)
            content: Content to write
            
        Returns:
            True if successful
        """
        full_path = self.workspace_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        self._log(f"📝 Writing: {full_path}")
        
        action = FileWriteAction(path=str(full_path), content=content)
        observation = await self.runtime.run_action(action)
        
        success = isinstance(observation, FileWriteObservation)
        if success:
            self._log(f"✅ File written successfully")
        return success
    
    async def browse_url(self, url: str) -> Dict[str, Any]:
        """
        Browse a URL and get page content.
        
        Args:
            url: URL to browse
            
        Returns:
            Dictionary with page content and metadata
        """
        self._log(f"🌐 Browsing: {url}")
        
        action = BrowseURLAction(url=url)
        observation = await self.runtime.run_action(action)
        
        if isinstance(observation, BrowserOutputObservation):
            return {
                "url": observation.url,
                "content": observation.content,
                "screenshot": observation.screenshot,
            }
        return {"content": str(observation)}
    
    async def ask(self, task: str, max_iterations: int = 10) -> State:
        """
        Ask OpenHands to complete a task using the full agent.
        
        Args:
            task: Task description
            max_iterations: Maximum agent iterations
            
        Returns:
            Final state with results
        """
        self._log(Panel(f"🤖 Task: {task}", title="OpenHands Agent"))
        
        state = await run_controller(
            config=self.config,
            initial_user_action=MessageAction(content=task),
            runtime=self.runtime,
            max_iterations=max_iterations,
        )
        
        self._log("✅ Task completed")
        return state
    
    async def code_task(
        self,
        task: str,
        language: str = "python",
        filename: str = None
    ) -> str:
        """
        Ask OpenHands to write code for a specific task.
        
        Args:
            task: Description of what the code should do
            language: Programming language
            filename: Optional filename to save the code
            
        Returns:
            Generated code
        """
        prompt = f"""Write {language} code to: {task}

Requirements:
- Write clean, well-documented code
- Include error handling
- Make it production-ready
- Only output the code, no explanations
"""
        
        state = await self.ask(prompt, max_iterations=5)
        
        # Extract code from the final state
        code = self._extract_code_from_state(state)
        
        if filename:
            await self.write_file(filename, code)
        
        return code
    
    def _extract_code_from_state(self, state: State) -> str:
        """Extract code from agent state."""
        # Look through history for file writes or code outputs
        for event in reversed(state.history):
            if hasattr(event, 'content') and '```' in str(event.content):
                content = str(event.content)
                # Extract code block
                start = content.find('```')
                end = content.rfind('```')
                if start != end:
                    code = content[start:end+3]
                    # Remove markdown code fence
                    lines = code.split('\n')
                    if lines[0].startswith('```'):
                        lines = lines[1:]
                    if lines[-1] == '```':
                        lines = lines[:-1]
                    return '\n'.join(lines)
        return ""


class OpenHandsSync:
    """
    Synchronous wrapper for OpenHands client.
    Use this if you don't want to deal with async/await.
    """
    
    def __init__(self, **kwargs):
        self._client = OpenHandsClient(**kwargs)
        self._loop = asyncio.new_event_loop()
    
    def _run(self, coro):
        return self._loop.run_until_complete(coro)
    
    def start(self):
        return self._run(self._client.start())
    
    def stop(self):
        return self._run(self._client.stop())
    
    def run_command(self, command: str) -> str:
        return self._run(self._client.run_command(command))
    
    def read_file(self, filepath: str) -> str:
        return self._run(self._client.read_file(filepath))
    
    def write_file(self, filepath: str, content: str) -> bool:
        return self._run(self._client.write_file(filepath, content))
    
    def browse_url(self, url: str) -> Dict[str, Any]:
        return self._run(self._client.browse_url(url))
    
    def ask(self, task: str, max_iterations: int = 10):
        return self._run(self._client.ask(task, max_iterations))
    
    def code_task(self, task: str, language: str = "python", filename: str = None) -> str:
        return self._run(self._client.code_task(task, language, filename))
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()


# Convenience function
def create_client(provider: str = "deepseek_local", **kwargs) -> OpenHandsSync:
    """
    Create a synchronous OpenHands client.
    
    Example:
        with create_client("deepseek_local") as client:
            result = client.run_command("ls -la")
            print(result)
    """
    return OpenHandsSync(provider=provider, **kwargs)
