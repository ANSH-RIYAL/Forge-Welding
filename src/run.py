"""
Main CLI Runner for Agentic Project Management Bot
Orchestrates all modules and provides the main entry point.
"""

import sys
import logging
import os
from typing import Dict, Any
import argparse

# Import our modules
from config_manager import load_and_validate_config, get_github_config, get_gemini_config, get_paths_config, get_logging_config, get_bot_config
from github_client import GitHubClient
from parser import parse_implementation_plan, extract_subtasks_as_dicts, get_plan_summary
from llm_planner import generate_tickets, compare_subtasks_with_issues, create_ticket_from_subtask


def setup_logging(config: Dict[str, Any]) -> None:
    """
    Setup logging configuration.
    
    Args:
        config: Configuration dictionary
    """
    logging_config = get_logging_config(config)
    paths_config = get_paths_config(config)
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(paths_config['log_file'])
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, logging_config.get('level', 'INFO')),
        format=logging_config.get('format', '%(asctime)s - %(levelname)s - %(message)s'),
        handlers=[
            logging.FileHandler(paths_config['log_file'], mode=logging_config.get('file_mode', 'w')),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")


def test_github_connection(github_config: Dict[str, Any]) -> bool:
    """
    Test GitHub API connection and permissions.
    
    Args:
        github_config: GitHub configuration
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        success = client.test_connection()
        if success:
            # Get repository info
            repo_info = client.get_repository_info()
            print(f"✅ Connected to repository: {repo_info.get('full_name', 'Unknown')}")
            print(f"   Open issues: {repo_info.get('open_issues', 0)}")
            
            # Test project access if configured
            if github_config.get('project_id'):
                project = client.get_project()
                if project:
                    print(f"✅ Project access: {project.name}")
                else:
                    print("⚠️  Project access failed (this is optional)")
        
        return success
        
    except Exception as e:
        print(f"❌ GitHub connection failed: {e}")
        return False


def test_gemini_connection(gemini_config: Dict[str, Any]) -> bool:
    """
    Test Gemini API connection.
    
    Args:
        gemini_config: Gemini configuration
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        from llm_planner import setup_gemini_client
        
        model = setup_gemini_client(
            api_key=gemini_config['api_key'],
            model=gemini_config.get('model', 'gemini-1.5-flash')
        )
        
        # Test with a simple prompt
        response = model.generate_content("Hello, this is a test.")
        
        if response.text:
            print("✅ Gemini API connection successful")
            return True
        else:
            print("❌ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")
        return False


def run_bot(config: Dict[str, Any], dry_run: bool = False) -> bool:
    """
    Run the complete bot workflow.
    
    Args:
        config: Configuration dictionary
        dry_run: Whether to run in dry-run mode
        
    Returns:
        True if successful, False otherwise
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Extract configurations
        github_config = get_github_config(config)
        gemini_config = get_gemini_config(config)
        paths_config = get_paths_config(config)
        bot_config = get_bot_config(config)
        
        # Override dry_run if specified
        if dry_run:
            bot_config['dry_run'] = True
        
        logger.info("Starting Agentic Project Management Bot")
        print("🚀 Starting Agentic Project Management Bot...")
        
        # Step 1: Parse implementation plan
        logger.info("Step 1: Parsing implementation plan")
        print("📋 Step 1: Parsing implementation plan...")
        
        plan = parse_implementation_plan(paths_config['implementation_plan'])
        plan_summary = get_plan_summary(plan)
        
        print(f"   Project: {plan_summary['project_name']}")
        print(f"   Phases: {plan_summary['total_phases']}")
        print(f"   Tasks: {plan_summary['total_tasks']}")
        print(f"   Subtasks: {plan_summary['total_subtasks']}")
        print(f"   Total Points: {plan_summary['total_estimated_points']}")
        
        # Step 2: Fetch existing GitHub issues
        logger.info("Step 2: Fetching existing GitHub issues")
        print("🔍 Step 2: Fetching existing GitHub issues...")
        
        github_client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        existing_issues = github_client.fetch_all_issues(
            include_closed=bot_config.get('include_closed_issues', False)
        )
        
        print(f"   Found {len(existing_issues)} existing issues")
        
        # Step 3: Compare plan with existing issues
        logger.info("Step 3: Comparing plan with existing issues")
        print("🔍 Step 3: Comparing plan with existing issues...")
        
        subtasks = extract_subtasks_as_dicts(plan)
        missing_subtasks = compare_subtasks_with_issues(subtasks, existing_issues)
        
        print(f"   Found {len(missing_subtasks)} subtasks without corresponding issues")
        
        if not missing_subtasks:
            print("✅ All subtasks already have corresponding issues!")
            return True
        
        # Step 4: Generate new tickets using LLM
        logger.info("Step 4: Generating new tickets using LLM")
        print("🤖 Step 4: Generating new tickets using LLM...")
        
        if bot_config.get('dry_run', False):
            print("   DRY RUN MODE: Would generate tickets using LLM")
            # Create tickets directly from subtasks for dry run
            new_tickets = []
            for subtask in missing_subtasks[:bot_config.get('max_new_tickets', 10)]:
                ticket = create_ticket_from_subtask(subtask)
                new_tickets.append(ticket)
        else:
            new_tickets = generate_tickets(
                plan=plan,
                existing_issues=existing_issues,
                gemini_config=gemini_config,
                template_path=paths_config['prompt_template']
            )
        
        print(f"   Generated {len(new_tickets)} new tickets")
        
        # Step 5: Create GitHub issues
        logger.info("Step 5: Creating GitHub issues")
        print("📝 Step 5: Creating GitHub issues...")
        
        if bot_config.get('dry_run', False):
            print("   DRY RUN MODE: Would create the following issues:")
            for i, ticket in enumerate(new_tickets, 1):
                print(f"   {i}. {ticket['title']}")
                print(f"      Labels: {', '.join(ticket.get('labels', []))}")
                print(f"      Milestone: {ticket.get('milestone', 'None')}")
                print()
        else:
            created_issues = github_client.create_multiple_issues(new_tickets)
            print(f"   Created {len(created_issues)} issues on GitHub")
            
            # Add to project if configured
            if github_config.get('project_id'):
                project = github_client.get_project()
                if project:
                    for issue in created_issues:
                        github_client.add_issue_to_project(issue['number'], project)
                    print(f"   Added issues to project: {project.name}")
        
        logger.info("Bot execution completed successfully")
        print("✅ Bot execution completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Bot execution failed: {e}")
        print(f"❌ Bot execution failed: {e}")
        return False


def main():
    """
    Main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(description="Agentic Project Management Bot")
    parser.add_argument(
        "--config", 
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (don't create actual tickets)"
    )
    parser.add_argument(
        "--test-connections",
        action="store_true",
        help="Test API connections only"
    )
    
    args = parser.parse_args()
    
    try:
        # Load and validate configuration
        print("🔧 Loading configuration...")
        config = load_and_validate_config(args.config)
        print("✅ Configuration loaded and validated")
        
        # Setup logging
        setup_logging(config)
        
        # Extract configurations
        github_config = get_github_config(config)
        gemini_config = get_gemini_config(config)
        
        # Test connections if requested
        if args.test_connections:
            print("\n🧪 Testing API connections...")
            
            github_success = test_github_connection(github_config)
            gemini_success = test_gemini_connection(gemini_config)
            
            if github_success and gemini_success:
                print("\n✅ All connections successful!")
                return 0
            else:
                print("\n❌ Some connections failed!")
                return 1
        
        # Run the bot
        success = run_bot(config, dry_run=args.dry_run)
        return 0 if success else 1
        
    except FileNotFoundError as e:
        print(f"❌ Configuration file not found: {e}")
        print("Please copy config/config_template.yaml to config/config.yaml and fill in your API keys")
        return 1
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 