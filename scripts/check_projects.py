#!/usr/bin/env python3
"""
Simple script to check available projects in the repository
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from github_client import GitHubClient
from config_manager import load_and_validate_config

def main():
    print("🔧 Loading configuration...")
    config = load_and_validate_config()
    print("✅ Configuration loaded")
    
    print("🔍 Checking available projects...")
    github_cfg = config['github']
    api_token = github_cfg['api_token']
    repository = github_cfg['repository']
    project_id = github_cfg.get('project_id')
    client = GitHubClient(api_token, repository, project_id)
    
    try:
        # Try to get projects using REST API
        projects = client.get_projects()
        print(f"📋 Found {len(projects)} projects:")
        for project in projects:
            print(f"  #{project.number}: {project.name}")
    except Exception as e:
        print(f"❌ Error getting projects: {e}")
        
        # Try alternative method
        try:
            repo = client.github.get_repo(repository)
            print("📋 Repository info:")
            print(f"  Name: {repo.name}")
            print(f"  Full name: {repo.full_name}")
            print(f"  Private: {repo.private}")
        except Exception as e2:
            print(f"❌ Error getting repo info: {e2}")

if __name__ == "__main__":
    main() 