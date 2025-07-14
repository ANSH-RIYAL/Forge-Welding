"""
Create milestones for the project phases
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_manager import load_and_validate_config, get_github_config
from github_client import GitHubClient


def create_milestones():
    """Create milestones for different project phases."""
    
    config = load_and_validate_config()
    github_config = get_github_config(config)
    
    client = GitHubClient(
        api_token=github_config['api_token'],
        repository=github_config['repository'],
        project_id=github_config.get('project_id')
    )
    
    # Milestones for different phases
    milestones = [
        {
            'title': 'Data Collection & Initial Setup',
            'description': 'Begin work on data infrastructure and a local HTML interface.',
            'state': 'open'
        },
        {
            'title': 'Model Development',
            'description': 'Train and develop the core AI models for face recognition and emotion detection.',
            'state': 'open'
        },
        {
            'title': 'System Integration',
            'description': 'Connect all components and implement access control logic.',
            'state': 'open'
        },
        {
            'title': 'Storage Backend & Refactor',
            'description': 'Switch to cloud storage and clean up the codebase.',
            'state': 'open'
        }
    ]
    
    print("🎯 Creating milestones for project phases...")
    
    created_milestones = []
    for milestone in milestones:
        try:
            # Create milestone
            new_milestone = client.repo.create_milestone(
                title=milestone['title'],
                description=milestone['description'],
                state=milestone['state']
            )
            created_milestones.append(new_milestone)
            print(f"✅ Created milestone: {milestone['title']}")
        except Exception as e:
            print(f"❌ Failed to create milestone '{milestone['title']}': {e}")
    
    print(f"🎉 Successfully created {len(created_milestones)} milestones!")
    return created_milestones


if __name__ == "__main__":
    create_milestones() 