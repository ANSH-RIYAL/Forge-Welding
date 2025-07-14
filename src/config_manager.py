"""
Configuration Manager for Agentic Project Management Bot
Handles loading and validation of configuration files.
"""

import os
import yaml
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary containing configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
    """
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        logger.info(f"Configuration loaded from {config_path}")
        return config
        
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in configuration file: {e}")
        raise


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate required configuration fields.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    required_sections = ['gemini', 'github', 'paths', 'logging', 'bot']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required configuration section: {section}")
    
    # Validate Gemini configuration
    gemini_config = config['gemini']
    required_gemini_fields = ['api_key', 'model']
    for field in required_gemini_fields:
        if field not in gemini_config:
            raise ValueError(f"Missing required Gemini field: {field}")
    
    # Validate GitHub configuration
    github_config = config['github']
    required_github_fields = ['api_token', 'repository']
    for field in required_github_fields:
        if field not in github_config:
            raise ValueError(f"Missing required GitHub field: {field}")
    
    # Validate paths
    paths_config = config['paths']
    required_paths_fields = ['implementation_plan', 'prompt_template', 'log_file']
    for field in required_paths_fields:
        if field not in paths_config:
            raise ValueError(f"Missing required paths field: {field}")
    
    logger.info("Configuration validation passed")
    return True


def get_gemini_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract Gemini API configuration.
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Gemini configuration dictionary
    """
    return config.get('gemini', {})


def get_github_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract GitHub API configuration.
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        GitHub configuration dictionary
    """
    return config.get('github', {})


def get_paths_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract file paths configuration.
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Paths configuration dictionary
    """
    return config.get('paths', {})


def get_logging_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract logging configuration.
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Logging configuration dictionary
    """
    return config.get('logging', {})


def get_bot_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract bot behavior configuration.
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Bot configuration dictionary
    """
    return config.get('bot', {})


def validate_api_keys(config: Dict[str, Any]) -> bool:
    """
    Validate that API keys are not placeholder values.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    gemini_config = get_gemini_config(config)
    github_config = get_github_config(config)
    
    # Check Gemini API key
    gemini_key = gemini_config.get('api_key', '')
    if not gemini_key or gemini_key == "YOUR_GEMINI_API_KEY_HERE":
        raise ValueError("Gemini API key not configured. Please update config.yaml")
    
    # Check GitHub API token
    github_token = github_config.get('api_token', '')
    if not github_token or github_token == "YOUR_GITHUB_TOKEN_HERE":
        raise ValueError("GitHub API token not configured. Please update config.yaml")
    
    logger.info("API key validation passed")
    return True


def load_and_validate_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load and validate configuration in one step.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Validated configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
        ValueError: If configuration is invalid
    """
    config = load_config(config_path)
    validate_config(config)
    validate_api_keys(config)
    return config 