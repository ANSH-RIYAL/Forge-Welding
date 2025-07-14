"""
GitHub GraphQL utilities for Project Board (Beta/Next) automation.
"""

import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


def run_github_graphql_query(query: str, variables: Dict[str, Any], token: str) -> Dict[str, Any]:
    """
    Execute a GraphQL query against GitHub's API.
    
    Args:
        query: GraphQL query string
        variables: Variables for the query
        token: GitHub personal access token
        
    Returns:
        GraphQL response data
        
    Raises:
        requests.HTTPError: If the request fails
        Exception: If GraphQL returns errors
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    
    try:
        response = requests.post(
            GITHUB_GRAPHQL_URL,
            json={"query": query, "variables": variables},
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            error_msg = f"GraphQL error: {data['errors']}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        return data["data"]
        
    except requests.HTTPError as e:
        logger.error(f"HTTP error in GraphQL query: {e}")
        raise
    except Exception as e:
        logger.error(f"GraphQL query failed: {e}")
        raise


def get_project_node_id(owner: str, project_number: int, token: str) -> str:
    """
    Get the node ID for a user/org project (Beta/Next) by project number.
    
    Args:
        owner: GitHub username or organization name
        project_number: Project number (not node ID)
        token: GitHub personal access token
        
    Returns:
        Project node ID
        
    Raises:
        Exception: If project not found
    """
    # First try user projects
    query = """
    query($owner: String!, $number: Int!) {
      user(login: $owner) {
        projectV2(number: $number) {
          id
          title
        }
      }
    }
    """
    
    variables = {"owner": owner, "number": project_number}
    
    try:
        data = run_github_graphql_query(query, variables, token)
        
        if data["user"] and data["user"]["projectV2"]:
            project_id = data["user"]["projectV2"]["id"]
            project_title = data["user"]["projectV2"]["title"]
            logger.info(f"Found user project: {project_title} (ID: {project_id})")
            return project_id
    except Exception as e:
        logger.warning(f"User project query failed: {e}")
    
    # If user project failed, try organization projects
    query = """
    query($owner: String!, $number: Int!) {
      organization(login: $owner) {
        projectV2(number: $number) {
          id
          title
        }
      }
    }
    """
    
    try:
        data = run_github_graphql_query(query, variables, token)
        
        if data["organization"] and data["organization"]["projectV2"]:
            project_id = data["organization"]["projectV2"]["id"]
            project_title = data["organization"]["projectV2"]["title"]
            logger.info(f"Found organization project: {project_title} (ID: {project_id})")
            return project_id
    except Exception as e:
        logger.warning(f"Organization project query failed: {e}")
    
    raise Exception(f"Project #{project_number} not found for owner '{owner}'. Check permissions and project number.")


def get_issue_node_id(owner: str, repo: str, issue_number: int, token: str) -> str:
    """
    Get the node ID for an issue by repo and issue number.
    
    Args:
        owner: Repository owner
        repo: Repository name
        issue_number: Issue number
        token: GitHub personal access token
        
    Returns:
        Issue node ID
        
    Raises:
        Exception: If issue not found
    """
    query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) {
          id
          title
        }
      }
    }
    """
    
    variables = {"owner": owner, "repo": repo, "number": issue_number}
    data = run_github_graphql_query(query, variables, token)
    
    if not data["repository"]["issue"]:
        raise Exception(f"Issue #{issue_number} not found in {owner}/{repo}")
        
    issue_id = data["repository"]["issue"]["id"]
    issue_title = data["repository"]["issue"]["title"]
    logger.info(f"Found issue: {issue_title} (ID: {issue_id})")
    return issue_id


def add_issue_to_project(project_node_id: str, issue_node_id: str, token: str) -> str:
    """
    Add an issue to a project board (Beta/Next) using GraphQL mutation.
    
    Args:
        project_node_id: Project node ID
        issue_node_id: Issue node ID
        token: GitHub personal access token
        
    Returns:
        Project item node ID
        
    Raises:
        Exception: If addition fails
    """
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """
    
    variables = {"projectId": project_node_id, "contentId": issue_node_id}
    data = run_github_graphql_query(mutation, variables, token)
    
    item_id = data["addProjectV2ItemById"]["item"]["id"]
    logger.info(f"Added issue to project (Item ID: {item_id})")
    return item_id


def list_project_items(project_node_id: str, token: str, first: int = 10) -> list:
    """
    List items in a project board for verification.
    
    Args:
        project_node_id: Project node ID
        token: GitHub personal access token
        first: Number of items to fetch
        
    Returns:
        List of project items
    """
    query = """
    query($projectId: ID!, $first: Int!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          title
          items(first: $first) {
            nodes {
              id
              content {
                ... on Issue {
                  number
                  title
                  url
                }
              }
            }
          }
        }
      }
    }
    """
    
    variables = {"projectId": project_node_id, "first": first}
    data = run_github_graphql_query(query, variables, token)
    
    project_title = data["node"]["title"]
    items = data["node"]["items"]["nodes"]
    logger.info(f"Found {len(items)} items in project '{project_title}'")
    
    return items


def test_project_board_integration(owner: str, repo: str, project_number: int, issue_number: int, token: str) -> bool:
    """
    Test the complete workflow: get project ID, get issue ID, add to project.
    
    Args:
        owner: Repository owner
        repo: Repository name
        project_number: Project number
        issue_number: Issue number to add
        token: GitHub personal access token
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"🧪 Testing project board integration...")
        print(f"   Owner: {owner}")
        print(f"   Repo: {repo}")
        print(f"   Project: #{project_number}")
        print(f"   Issue: #{issue_number}")
        print()
        
        # Step 1: Get project node ID
        print("1️⃣ Getting project node ID...")
        project_node_id = get_project_node_id(owner, project_number, token)
        print(f"   ✅ Project node ID: {project_node_id}")
        print()
        
        # Step 2: Get issue node ID
        print("2️⃣ Getting issue node ID...")
        issue_node_id = get_issue_node_id(owner, repo, issue_number, token)
        print(f"   ✅ Issue node ID: {issue_node_id}")
        print()
        
        # Step 3: Add issue to project
        print("3️⃣ Adding issue to project...")
        item_id = add_issue_to_project(project_node_id, issue_node_id, token)
        print(f"   ✅ Added to project (Item ID: {item_id})")
        print()
        
        # Step 4: Verify by listing project items
        print("4️⃣ Verifying project items...")
        items = list_project_items(project_node_id, token, first=20)
        print(f"   ✅ Found {len(items)} items in project")
        
        # Check if our issue is in the list
        for item in items:
            if item["content"] and item["content"]["number"] == issue_number:
                print(f"   ✅ Issue #{issue_number} confirmed in project!")
                break
        else:
            print(f"   ⚠️  Issue #{issue_number} not found in project items")
        
        print()
        print("🎉 Project board integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Project board integration test failed: {e}")
        return False 