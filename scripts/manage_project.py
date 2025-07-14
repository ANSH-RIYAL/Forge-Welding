#!/usr/bin/env python3
"""
Script to list all projects (classic and beta/next) for the user and repository.
If no project exists, create a new (beta/next) project for the repository.
Outputs project details and node IDs for automation.
"""
import sys
import os
import requests
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from github import Github
from config_manager import load_and_validate_config

def list_classic_projects(repo):
    print("\n📋 Classic Projects:")
    try:
        projects = list(repo.get_projects())
        if not projects:
            print("  (none)")
        for p in projects:
            print(f"  [Classic] #{p.number}: {p.name} (id={p.id})")
    except Exception as e:
        print(f"  Error listing classic projects: {e}")

def list_beta_projects(api_token, owner, repo_name):
    print("\n🧩 Beta/Next Projects (GraphQL):")
    headers = {"Authorization": f"Bearer {api_token}"}
    # List repository projects (beta/next)
    query = '''
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        projectsV2(first: 10) {
          nodes {
            id
            title
            number
            closed
            public
          }
        }
      }
    }
    '''
    variables = {"owner": owner, "repo": repo_name}
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    data = resp.json()
    try:
        nodes = data['data']['repository']['projectsV2']['nodes']
        if not nodes:
            print("  (none)")
        for p in nodes:
            print(f"  [Beta] #{p['number']}: {p['title']} (id={p['id']}){' [closed]' if p['closed'] else ''}")
        return nodes
    except Exception as e:
        print(f"  Error listing beta/next projects: {e}\n  Raw: {data}")
        return []

def create_beta_project(api_token, owner, repo_name):
    print("\n🚀 Creating new Beta/Next project...")
    headers = {"Authorization": f"Bearer {api_token}"}
    mutation = '''
    mutation($input: CreateProjectV2Input!) {
      createProjectV2(input: $input) {
        projectV2 {
          id
          title
          number
        }
      }
    }
    '''
    variables = {
        "input": {
            "ownerId": None,  # Will fill in below
            "title": "Agentic Project Board"
        }
    }
    # Get repository node ID
    repo_query = '''
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) { id }
    }
    '''
    repo_resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": repo_query, "variables": {"owner": owner, "repo": repo_name}},
        headers=headers
    )
    repo_data = repo_resp.json()
    try:
        repo_id = repo_data['data']['repository']['id']
        variables['input']['repositoryId'] = repo_id
        del variables['input']['ownerId']
    except Exception as e:
        print(f"  Error getting repository node ID: {e}\n  Raw: {repo_data}")
        return None
    # Create the project
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": mutation, "variables": variables},
        headers=headers
    )
    data = resp.json()
    try:
        proj = data['data']['createProjectV2']['projectV2']
        print(f"  Created [Beta] #{proj['number']}: {proj['title']} (id={proj['id']})")
        return proj
    except Exception as e:
        print(f"  Error creating beta/next project: {e}\n  Raw: {data}")
        return None

def main():
    config = load_and_validate_config()
    github_cfg = config['github']
    api_token = github_cfg['api_token']
    repository = github_cfg['repository']
    owner, repo_name = repository.split('/')
    g = Github(api_token)
    repo = g.get_repo(repository)
    list_classic_projects(repo)
    beta_projects = list_beta_projects(api_token, owner, repo_name)
    if not beta_projects:
        proj = create_beta_project(api_token, owner, repo_name)
        if proj:
            print(f"\n✅ Project created: [Beta] #{proj['number']}: {proj['title']} (id={proj['id']})")
        else:
            print("❌ Failed to create project.")
    else:
        print("\n✅ At least one project exists. No need to create a new one.")

if __name__ == "__main__":
    main() 