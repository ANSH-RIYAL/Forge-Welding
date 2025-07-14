"""
Agentic Project Management Bot
A bot that automatically generates GitHub issues from YAML implementation plans using LLM.
"""

__version__ = "1.0.0"
__author__ = "ANSH-RIYAL"
__description__ = "Agentic Project Management Bot for GitHub issue generation"

# Import main modules for easy access
from .config_manager import load_and_validate_config
from .github_client import GitHubClient
from .parser import parse_implementation_plan, extract_subtasks_as_dicts
from .llm_planner import generate_tickets, setup_gemini_client
from .run import main, run_bot

__all__ = [
    'load_and_validate_config',
    'GitHubClient',
    'parse_implementation_plan',
    'extract_subtasks_as_dicts',
    'generate_tickets',
    'setup_gemini_client',
    'main',
    'run_bot'
] 