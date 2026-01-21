"""
OpenHands SDK Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_CONFIG = {
    # DeepSeek Local (via Ollama) - Default
    "deepseek_local": {
        "model": "ollama/deepseek-coder-v2:16b",
        "api_key": "ollama",
        "base_url": "http://localhost:11434",
    },
    # DeepSeek API (Cloud)
    "deepseek_api": {
        "model": "deepseek-chat",
        "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
        "base_url": "https://api.deepseek.com/v1",
    },
    # OpenAI
    "openai": {
        "model": "gpt-4o",
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "base_url": "https://api.openai.com/v1",
    },
    # Anthropic
    "anthropic": {
        "model": "claude-sonnet-4-20250514",
        "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
        "base_url": "https://api.anthropic.com",
    },
}

# Default provider
DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek_local")

# Workspace configuration
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "./workspace")

# OpenHands server (if using remote)
OPENHANDS_SERVER_URL = os.getenv("OPENHANDS_SERVER_URL", "http://localhost:3000")


def get_llm_config(provider: str = None):
    """Get LLM configuration for specified provider."""
    provider = provider or DEFAULT_PROVIDER
    if provider not in LLM_CONFIG:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(LLM_CONFIG.keys())}")
    return LLM_CONFIG[provider]
