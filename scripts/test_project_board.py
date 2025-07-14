"""
Simple test script for project board integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_manager import load_and_validate_config, get_github_config
from github_graphql import test_project_board_integration


def main():
    """Test adding a single issue to the project board."""
    
    try:
        # Load configuration
        print("🔧 Loading configuration...")
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        # Extract values
        token = github_config['api_token']
        repository = github_config['repository']
        project_id = github_config.get('project_id', 3)
        
        # Parse repository
        owner, repo = repository.split('/')
        
        print(f"✅ Configuration loaded")
        print(f"   Repository: {repository}")
        print(f"   Project ID: {project_id}")
        print()
        
        # Test with issue #2 (one of the example tickets we created)
        issue_number = 2
        
        # Run the test
        success = test_project_board_integration(
            owner=owner,
            repo=repo,
            project_number=project_id,
            issue_number=issue_number,
            token=token
        )
        
        if success:
            print("🎉 Test completed successfully!")
            print("Check your project board at: https://github.com/users/ANSH-RIYAL/projects/3/views/1")
        else:
            print("❌ Test failed!")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")


if __name__ == "__main__":
    main() 