"""
Parser for Agentic Project Management Bot
Handles YAML implementation plan parsing and data extraction.
"""

import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Subtask:
    """Data class for representing a subtask."""
    name: str
    description: str
    estimated_points: int
    labels: List[str]
    phase_name: str
    task_name: str


def parse_implementation_plan(file_path: str) -> Dict[str, Any]:
    """
    Parse YAML implementation plan file.
    
    Args:
        file_path: Path to the YAML implementation plan file
        
    Returns:
        Parsed implementation plan dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If file is invalid YAML
        ValueError: If plan structure is invalid
    """
    try:
        with open(file_path, 'r') as file:
            plan = yaml.safe_load(file)
        
        logger.info(f"Implementation plan loaded from {file_path}")
        
        # Validate the plan structure
        validate_plan_structure(plan)
        
        return plan
        
    except FileNotFoundError as e:
        logger.error(f"Implementation plan file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in implementation plan: {e}")
        raise


def validate_plan_structure(plan: Dict[str, Any]) -> bool:
    """
    Validate the structure of an implementation plan.
    
    Args:
        plan: Implementation plan dictionary
        
    Returns:
        True if valid, raises ValueError if invalid
        
    Raises:
        ValueError: If plan structure is invalid
    """
    # Check for required top-level fields
    if 'project' not in plan:
        raise ValueError("Implementation plan must have a 'project' field")
    
    if 'phases' not in plan:
        raise ValueError("Implementation plan must have a 'phases' field")
    
    if not isinstance(plan['phases'], list):
        raise ValueError("'phases' must be a list")
    
    # Validate each phase
    for i, phase in enumerate(plan['phases']):
        if not isinstance(phase, dict):
            raise ValueError(f"Phase {i} must be a dictionary")
        
        if 'name' not in phase:
            raise ValueError(f"Phase {i} must have a 'name' field")
        
        if 'tasks' not in phase:
            raise ValueError(f"Phase {i} must have a 'tasks' field")
        
        if not isinstance(phase['tasks'], list):
            raise ValueError(f"Tasks in phase {i} must be a list")
        
        # Validate each task
        for j, task in enumerate(phase['tasks']):
            if not isinstance(task, dict):
                raise ValueError(f"Task {j} in phase {i} must be a dictionary")
            
            if 'name' not in task:
                raise ValueError(f"Task {j} in phase {i} must have a 'name' field")
            
            if 'subtasks' not in task:
                raise ValueError(f"Task {j} in phase {i} must have a 'subtasks' field")
            
            if not isinstance(task['subtasks'], list):
                raise ValueError(f"Subtasks in task {j} of phase {i} must be a list")
            
            # Validate each subtask
            for k, subtask in enumerate(task['subtasks']):
                if not isinstance(subtask, dict):
                    raise ValueError(f"Subtask {k} in task {j} of phase {i} must be a dictionary")
                
                if 'name' not in subtask:
                    raise ValueError(f"Subtask {k} in task {j} of phase {i} must have a 'name' field")
                
                if 'description' not in subtask:
                    raise ValueError(f"Subtask {k} in task {j} of phase {i} must have a 'description' field")
                
                if 'estimated_points' not in subtask:
                    raise ValueError(f"Subtask {k} in task {j} of phase {i} must have an 'estimated_points' field")
                
                if 'labels' not in subtask:
                    raise ValueError(f"Subtask {k} in task {j} of phase {i} must have a 'labels' field")
                
                if not isinstance(subtask['labels'], list):
                    raise ValueError(f"Labels in subtask {k} of task {j} in phase {i} must be a list")
    
    logger.info("Implementation plan structure validation passed")
    return True


def extract_subtasks(plan: Dict[str, Any]) -> List[Subtask]:
    """
    Extract all subtasks from the implementation plan.
    
    Args:
        plan: Implementation plan dictionary
        
    Returns:
        List of Subtask objects
    """
    subtasks = []
    
    for phase in plan['phases']:
        phase_name = phase['name']
        
        for task in phase['tasks']:
            task_name = task['name']
            
            for subtask in task['subtasks']:
                subtask_obj = Subtask(
                    name=subtask['name'],
                    description=subtask['description'],
                    estimated_points=subtask['estimated_points'],
                    labels=subtask['labels'],
                    phase_name=phase_name,
                    task_name=task_name
                )
                subtasks.append(subtask_obj)
    
    logger.info(f"Extracted {len(subtasks)} subtasks from implementation plan")
    return subtasks


def extract_subtasks_as_dicts(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract all subtasks from the implementation plan as dictionaries.
    
    Args:
        plan: Implementation plan dictionary
        
    Returns:
        List of subtask dictionaries
    """
    subtasks = []
    
    for phase in plan['phases']:
        phase_name = phase['name']
        
        for task in phase['tasks']:
            task_name = task['name']
            
            for subtask in task['subtasks']:
                subtask_dict = {
                    'name': subtask['name'],
                    'description': subtask['description'],
                    'estimated_points': subtask['estimated_points'],
                    'labels': subtask['labels'],
                    'phase_name': phase_name,
                    'task_name': task_name
                }
                subtasks.append(subtask_dict)
    
    logger.info(f"Extracted {len(subtasks)} subtasks as dictionaries")
    return subtasks


def get_phase_names(plan: Dict[str, Any]) -> List[str]:
    """
    Get all phase names from the implementation plan.
    
    Args:
        plan: Implementation plan dictionary
        
    Returns:
        List of phase names
    """
    phase_names = [phase['name'] for phase in plan['phases']]
    logger.info(f"Found {len(phase_names)} phases: {phase_names}")
    return phase_names


def get_task_names(plan: Dict[str, Any]) -> List[str]:
    """
    Get all task names from the implementation plan.
    
    Args:
        plan: Implementation plan dictionary
        
    Returns:
        List of task names
    """
    task_names = []
    for phase in plan['phases']:
        for task in phase['tasks']:
            task_names.append(task['name'])
    
    logger.info(f"Found {len(task_names)} tasks")
    return task_names


def get_subtask_names(plan: Dict[str, Any]) -> List[str]:
    """
    Get all subtask names from the implementation plan.
    
    Args:
        plan: Implementation plan dictionary
        
    Returns:
        List of subtask names
    """
    subtask_names = []
    for phase in plan['phases']:
        for task in phase['tasks']:
            for subtask in task['subtasks']:
                subtask_names.append(subtask['name'])
    
    logger.info(f"Found {len(subtask_names)} subtasks")
    return subtask_names


def find_subtask_by_name(plan: Dict[str, Any], subtask_name: str) -> Optional[Dict[str, Any]]:
    """
    Find a specific subtask by name.
    
    Args:
        plan: Implementation plan dictionary
        subtask_name: Name of the subtask to find
        
    Returns:
        Subtask dictionary or None if not found
    """
    for phase in plan['phases']:
        for task in phase['tasks']:
            for subtask in task['subtasks']:
                if subtask['name'] == subtask_name:
                    return {
                        'name': subtask['name'],
                        'description': subtask['description'],
                        'estimated_points': subtask['estimated_points'],
                        'labels': subtask['labels'],
                        'phase_name': phase['name'],
                        'task_name': task['name']
                    }
    
    logger.warning(f"Subtask '{subtask_name}' not found")
    return None


def get_subtasks_by_phase(plan: Dict[str, Any], phase_name: str) -> List[Dict[str, Any]]:
    """
    Get all subtasks for a specific phase.
    
    Args:
        plan: Implementation plan dictionary
        phase_name: Name of the phase
        
    Returns:
        List of subtask dictionaries for the phase
    """
    subtasks = []
    
    for phase in plan['phases']:
        if phase['name'] == phase_name:
            for task in phase['tasks']:
                for subtask in task['subtasks']:
                    subtask_dict = {
                        'name': subtask['name'],
                        'description': subtask['description'],
                        'estimated_points': subtask['estimated_points'],
                        'labels': subtask['labels'],
                        'phase_name': phase['name'],
                        'task_name': task['name']
                    }
                    subtasks.append(subtask_dict)
            break
    
    logger.info(f"Found {len(subtasks)} subtasks for phase '{phase_name}'")
    return subtasks


def get_subtasks_by_task(plan: Dict[str, Any], task_name: str) -> List[Dict[str, Any]]:
    """
    Get all subtasks for a specific task.
    
    Args:
        plan: Implementation plan dictionary
        task_name: Name of the task
        
    Returns:
        List of subtask dictionaries for the task
    """
    subtasks = []
    
    for phase in plan['phases']:
        for task in phase['tasks']:
            if task['name'] == task_name:
                for subtask in task['subtasks']:
                    subtask_dict = {
                        'name': subtask['name'],
                        'description': subtask['description'],
                        'estimated_points': subtask['estimated_points'],
                        'labels': subtask['labels'],
                        'phase_name': phase['name'],
                        'task_name': task['name']
                    }
                    subtasks.append(subtask_dict)
                break
    
    logger.info(f"Found {len(subtasks)} subtasks for task '{task_name}'")
    return subtasks


def get_subtasks_by_label(plan: Dict[str, Any], label: str) -> List[Dict[str, Any]]:
    """
    Get all subtasks with a specific label.
    
    Args:
        plan: Implementation plan dictionary
        label: Label to search for
        
    Returns:
        List of subtask dictionaries with the label
    """
    subtasks = []
    
    for phase in plan['phases']:
        for task in phase['tasks']:
            for subtask in task['subtasks']:
                if label in subtask['labels']:
                    subtask_dict = {
                        'name': subtask['name'],
                        'description': subtask['description'],
                        'estimated_points': subtask['estimated_points'],
                        'labels': subtask['labels'],
                        'phase_name': phase['name'],
                        'task_name': task['name']
                    }
                    subtasks.append(subtask_dict)
    
    logger.info(f"Found {len(subtasks)} subtasks with label '{label}'")
    return subtasks


def get_plan_summary(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of the implementation plan.
    
    Args:
        plan: Implementation plan dictionary
        
    Returns:
        Summary dictionary
    """
    subtasks = extract_subtasks_as_dicts(plan)
    
    summary = {
        'project_name': plan['project'],
        'total_phases': len(plan['phases']),
        'total_tasks': sum(len(phase['tasks']) for phase in plan['phases']),
        'total_subtasks': len(subtasks),
        'total_estimated_points': sum(subtask['estimated_points'] for subtask in subtasks),
        'phases': [phase['name'] for phase in plan['phases']],
        'all_labels': list(set(label for subtask in subtasks for label in subtask['labels']))
    }
    
    logger.info(f"Plan summary: {summary['total_subtasks']} subtasks, {summary['total_estimated_points']} total points")
    return summary 