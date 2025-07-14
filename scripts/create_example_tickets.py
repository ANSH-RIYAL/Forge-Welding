"""
Create example tickets to demonstrate the agent's workflow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_manager import load_and_validate_config, get_github_config
from github_client import GitHubClient


def create_example_tickets():
    """Create example tickets for different phases of the project."""
    
    config = load_and_validate_config()
    github_config = get_github_config(config)
    
    client = GitHubClient(
        api_token=github_config['api_token'],
        repository=github_config['repository'],
        project_id=github_config.get('project_id')
    )
    
    # Example tickets for different phases
    example_tickets = [
        {
            'title': 'Setup basic HTML local storage interface',
            'body': """This subtask belongs to:
- Phase: Data Collection & Initial Setup
- Task: Setup basic HTML local storage interface

Objective:
Create the initial web interface for the system with basic HTML form and camera capture placeholder.

Estimated Story Points: 2
Labels: frontend, ui
Complexity: low

Acceptance Criteria:
- [ ] Create responsive HTML page with login form
- [ ] Add camera capture placeholder
- [ ] Implement basic styling
- [ ] Test on different browsers""",
            'labels': ['frontend', 'ui'],
            'milestone': 'Data Collection & Initial Setup'
        },
        {
            'title': 'Add placeholder image capture for webcam',
            'body': """This subtask belongs to:
- Phase: Data Collection & Initial Setup
- Task: Setup basic HTML local storage interface

Objective:
Implement basic webcam access and image capture functionality for the face recognition system.

Estimated Story Points: 3
Labels: frontend, camera
Complexity: medium

Acceptance Criteria:
- [ ] Implement webcam access using getUserMedia API
- [ ] Add image capture functionality
- [ ] Display captured image preview
- [ ] Handle camera permissions
- [ ] Test on different devices""",
            'labels': ['frontend', 'camera'],
            'milestone': 'Data Collection & Initial Setup'
        },
        {
            'title': 'Collect sample facial data',
            'body': """This subtask belongs to:
- Phase: Model Development
- Task: Train Face ID Model

Objective:
Gather diverse facial images for training dataset to ensure robust face recognition.

Estimated Story Points: 5
Labels: ml, data-collection
Complexity: high

Acceptance Criteria:
- [ ] Collect 1000+ diverse facial images
- [ ] Ensure data quality and diversity
- [ ] Organize data for training pipeline
- [ ] Validate data format and structure
- [ ] Create data augmentation pipeline""",
            'labels': ['ml', 'data-collection'],
            'milestone': 'Model Development'
        },
        {
            'title': 'Train on face embedding matching',
            'body': """This subtask belongs to:
- Phase: Model Development
- Task: Train Face ID Model

Objective:
Implement and train face embedding model for accurate facial recognition.

Estimated Story Points: 8
Labels: ml, training
Complexity: high

Acceptance Criteria:
- [ ] Implement face embedding architecture
- [ ] Train model on collected dataset
- [ ] Achieve >95% accuracy on test set
- [ ] Optimize model performance
- [ ] Document training process""",
            'labels': ['ml', 'training'],
            'milestone': 'Model Development'
        },
        {
            'title': 'Load Face ID model in browser/backend',
            'body': """This subtask belongs to:
- Phase: System Integration
- Task: Connect models to frontend

Objective:
Integrate facial recognition model with web application for real-time face detection.

Estimated Story Points: 4
Labels: integration, frontend
Complexity: medium

Acceptance Criteria:
- [ ] Load model in browser environment
- [ ] Implement real-time face detection
- [ ] Optimize model for web performance
- [ ] Handle model loading errors
- [ ] Test integration thoroughly""",
            'labels': ['integration', 'frontend'],
            'milestone': 'System Integration'
        },
        {
            'title': 'Block access unless emotion is angry',
            'body': """This subtask belongs to:
- Phase: System Integration
- Task: Access control logic

Objective:
Implement emotion-based access control system that only grants access when user shows 'angry' expression.

Estimated Story Points: 4
Labels: security, logic
Complexity: medium

Acceptance Criteria:
- [ ] Implement emotion detection logic
- [ ] Create access control mechanism
- [ ] Test with different emotions
- [ ] Ensure security robustness
- [ ] Add logging for access attempts""",
            'labels': ['security', 'logic'],
            'milestone': 'System Integration'
        }
    ]
    
    print("🎯 Creating example tickets for demonstration...")
    
    created_issues = []
    for i, ticket in enumerate(example_tickets, 1):
        try:
            created_issue = client.create_issue(
                title=ticket['title'],
                body=ticket['body'],
                labels=ticket['labels'],
                milestone=ticket['milestone'],
                assignees=[]
            )
            created_issues.append(created_issue)
            print(f"✅ Created ticket #{created_issue['number']}: {ticket['title']}")
            print(f"   Labels: {', '.join(ticket['labels'])}")
            print(f"   Milestone: {ticket['milestone']}")
            print()
        except Exception as e:
            print(f"❌ Failed to create ticket '{ticket['title']}': {e}")
    
    print(f"🎉 Successfully created {len(created_issues)} example tickets!")
    return created_issues


if __name__ == "__main__":
    create_example_tickets() 