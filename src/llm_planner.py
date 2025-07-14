"""
LLM Planner for Agentic Project Management Bot
Handles Gemini API integration for ticket generation.
"""

import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import logging
import yaml

logger = logging.getLogger(__name__)


def setup_gemini_client(api_key: str, model: str = "gemini-1.5-flash") -> genai.GenerativeModel:
    """
    Setup Gemini API client.
    
    Args:
        api_key: Gemini API key
        model: Model to use
        
    Returns:
        Configured Gemini model
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model)
        logger.info(f"Gemini client initialized with model: {model}")
        return model
        
    except Exception as e:
        logger.error(f"Failed to setup Gemini client: {e}")
        raise


def load_prompt_template(template_path: str) -> Dict[str, str]:
    """
    Load prompt template from YAML file.
    
    Args:
        template_path: Path to prompt template file
        
    Returns:
        Dictionary with system_prompt and user_prompt_template
    """
    try:
        with open(template_path, 'r') as file:
            template = yaml.safe_load(file)
        
        logger.info(f"Prompt template loaded from {template_path}")
        return template
        
    except Exception as e:
        logger.error(f"Failed to load prompt template: {e}")
        raise


def create_prompt(plan: Dict[str, Any], existing_issues: List[Dict[str, Any]], 
                 template: Dict[str, str]) -> str:
    """
    Create the complete prompt for the LLM.
    
    Args:
        plan: Implementation plan dictionary
        existing_issues: List of existing GitHub issues
        template: Prompt template dictionary
        
    Returns:
        Complete prompt string
    """
    try:
        # Convert plan to YAML string
        plan_yaml = yaml.dump(plan, default_flow_style=False, sort_keys=False)
        
        # Convert existing issues to JSON string
        issues_json = json.dumps(existing_issues, indent=2)
        
        # Create user prompt by filling template
        user_prompt = template['user_prompt_template'].format(
            implementation_plan=plan_yaml,
            existing_issues=issues_json
        )
        
        # Combine system and user prompts
        complete_prompt = f"{template['system_prompt']}\n\n{user_prompt}"
        
        logger.info("Prompt created successfully")
        return complete_prompt
        
    except Exception as e:
        logger.error(f"Failed to create prompt: {e}")
        raise


def generate_tickets(plan: Dict[str, Any], existing_issues: List[Dict[str, Any]], 
                    gemini_config: Dict[str, Any], template_path: str) -> List[Dict[str, Any]]:
    """
    Generate new tickets using Gemini LLM.
    
    Args:
        plan: Implementation plan dictionary
        existing_issues: List of existing GitHub issues
        gemini_config: Gemini API configuration
        template_path: Path to prompt template file
        
    Returns:
        List of new ticket dictionaries
    """
    try:
        # Setup Gemini client
        model = setup_gemini_client(
            api_key=gemini_config['api_key'],
            model=gemini_config.get('model', 'gemini-1.5-flash')
        )
        
        # Load prompt template
        template = load_prompt_template(template_path)
        
        # Create prompt
        prompt = create_prompt(plan, existing_issues, template)
        
        # Generate response
        logger.info("Sending request to Gemini API...")
        response = model.generate_content(prompt)
        
        # Parse response
        new_tickets = parse_llm_response(response.text)
        
        logger.info(f"Generated {len(new_tickets)} new tickets")
        return new_tickets
        
    except Exception as e:
        logger.error(f"Failed to generate tickets: {e}")
        raise


def parse_llm_response(response_text: str) -> List[Dict[str, Any]]:
    """
    Parse LLM response to extract ticket data.
    
    Args:
        response_text: Raw response from LLM
        
    Returns:
        List of ticket dictionaries
    """
    try:
        # Try to extract JSON from response
        # Look for JSON array in the response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']')
        
        if start_idx == -1 or end_idx == -1:
            logger.error("No JSON array found in LLM response")
            return []
        
        json_str = response_text[start_idx:end_idx + 1]
        
        # Parse JSON
        tickets = json.loads(json_str)
        
        # Validate ticket structure
        validated_tickets = []
        for ticket in tickets:
            if validate_ticket_structure(ticket):
                validated_tickets.append(ticket)
            else:
                logger.warning(f"Invalid ticket structure: {ticket}")
        
        logger.info(f"Parsed {len(validated_tickets)} valid tickets from LLM response")
        return validated_tickets
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {e}")
        logger.error(f"Response text: {response_text}")
        return []
    except Exception as e:
        logger.error(f"Failed to parse LLM response: {e}")
        return []


def validate_ticket_structure(ticket: Dict[str, Any]) -> bool:
    """
    Validate that a ticket has the required structure.
    
    Args:
        ticket: Ticket dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['title', 'body']
    
    for field in required_fields:
        if field not in ticket:
            logger.warning(f"Missing required field '{field}' in ticket")
            return False
    
    # Validate title is not empty
    if not ticket['title'] or not ticket['title'].strip():
        logger.warning("Ticket title is empty")
        return False
    
    # Validate body is not empty
    if not ticket['body'] or not ticket['body'].strip():
        logger.warning("Ticket body is empty")
        return False
    
    # Validate labels if present
    if 'labels' in ticket and not isinstance(ticket['labels'], list):
        logger.warning("Ticket labels must be a list")
        return False
    
    return True


def format_ticket_for_github(ticket: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a ticket for GitHub API creation.
    
    Args:
        ticket: Raw ticket dictionary
        
    Returns:
        Formatted ticket for GitHub API
    """
    formatted_ticket = {
        'title': ticket['title'].strip(),
        'body': ticket['body'].strip()
    }
    
    # Add labels if present
    if 'labels' in ticket and ticket['labels']:
        formatted_ticket['labels'] = ticket['labels']
    
    # Add milestone if present
    if 'milestone' in ticket and ticket['milestone']:
        formatted_ticket['milestone'] = ticket['milestone']
    
    # Add assignees if present
    if 'assignees' in ticket and ticket['assignees']:
        formatted_ticket['assignees'] = ticket['assignees']
    
    return formatted_ticket


def compare_subtasks_with_issues(subtasks: List[Dict[str, Any]], 
                                existing_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compare subtasks with existing issues to find missing ones.
    
    Args:
        subtasks: List of subtasks from implementation plan
        existing_issues: List of existing GitHub issues
        
    Returns:
        List of subtasks that don't have corresponding issues
    """
    # Extract existing issue titles
    existing_titles = [issue['title'].lower().strip() for issue in existing_issues]
    
    # Find subtasks that don't have corresponding issues
    missing_subtasks = []
    
    for subtask in subtasks:
        subtask_title = subtask['name'].lower().strip()
        
        # Check if this subtask already has an issue
        has_issue = False
        for existing_title in existing_titles:
            if subtask_title in existing_title or existing_title in subtask_title:
                has_issue = True
                break
        
        if not has_issue:
            missing_subtasks.append(subtask)
    
    logger.info(f"Found {len(missing_subtasks)} subtasks without corresponding issues")
    return missing_subtasks


def estimate_ticket_complexity(subtask: Dict[str, Any]) -> str:
    """
    Estimate ticket complexity based on subtask data.
    
    Args:
        subtask: Subtask dictionary
        
    Returns:
        Complexity level (low, medium, high)
    """
    points = subtask.get('estimated_points', 1)
    
    if points <= 2:
        return "low"
    elif points <= 5:
        return "medium"
    else:
        return "high"


def generate_ticket_description(subtask: Dict[str, Any]) -> str:
    """
    Generate a detailed ticket description from subtask data.
    
    Args:
        subtask: Subtask dictionary
        
    Returns:
        Formatted description string
    """
    description = f"""This subtask belongs to:
- Phase: {subtask['phase_name']}
- Task: {subtask['task_name']}

Objective:
{subtask['description']}

Estimated Story Points: {subtask['estimated_points']}
Labels: {', '.join(subtask['labels'])}
Complexity: {estimate_ticket_complexity(subtask)}

Acceptance Criteria:
- [ ] Complete the described functionality
- [ ] Ensure code quality and documentation
- [ ] Test the implementation
- [ ] Update any related documentation"""
    
    return description


def create_ticket_from_subtask(subtask: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a GitHub ticket from a subtask.
    
    Args:
        subtask: Subtask dictionary
        
    Returns:
        GitHub ticket dictionary
    """
    ticket = {
        'title': subtask['name'],
        'body': generate_ticket_description(subtask),
        'labels': subtask['labels'],
        'milestone': subtask['phase_name'],
        'assignees': [],
        'state': 'open'
    }
    
    return ticket 