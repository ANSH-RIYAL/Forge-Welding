"""
Test GitHub token permissions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_manager import load_and_validate_config, get_github_config
from github_graphql import run_github_graphql_query


def test_token_permissions():
    """Test what permissions the current token has."""
    
    try:
        # Load configuration
        config = load_and_validate_config()
        github_config = get_github_config(config)
        token = github_config['api_token']
        
        print("🔧 Testing GitHub token permissions...")
        print()
        
        # Test 1: Basic user info
        print("1️⃣ Testing basic user access...")
        query = """
        query {
          viewer {
            login
            name
            email
          }
        }
        """
        
        try:
            data = run_github_graphql_query(query, {}, token)
            user = data["viewer"]
            print(f"   ✅ Connected as: {user['login']}")
            print(f"   ✅ Name: {user.get('name', 'N/A')}")
            print(f"   ✅ Email: {user.get('email', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Basic user access failed: {e}")
        
        print()
        
        # Test 2: Repository access
        print("2️⃣ Testing repository access...")
        owner, repo = github_config['repository'].split('/')
        query = """
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            name
            description
            isPrivate
            issues(first: 1) {
              totalCount
            }
          }
        }
        """
        
        try:
            data = run_github_graphql_query(query, {"owner": owner, "repo": repo}, token)
            repo_data = data["repository"]
            print(f"   ✅ Repository: {repo_data['name']}")
            print(f"   ✅ Private: {repo_data['isPrivate']}")
            print(f"   ✅ Issues count: {repo_data['issues']['totalCount']}")
        except Exception as e:
            print(f"   ❌ Repository access failed: {e}")
        
        print()
        
        # Test 3: Project access
        print("3️⃣ Testing project access...")
        project_number = github_config.get('project_id', 3)
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
        
        try:
            data = run_github_graphql_query(query, {"owner": owner, "number": project_number}, token)
            if data["user"] and data["user"]["projectV2"]:
                project = data["user"]["projectV2"]
                print(f"   ✅ Project access: {project['title']}")
                print(f"   ✅ Project ID: {project['id']}")
            else:
                print(f"   ⚠️  Project #{project_number} not found")
        except Exception as e:
            print(f"   ❌ Project access failed: {e}")
            print(f"   💡 You may need to add 'user' scope to your token")
        
        print()
        print("🎯 Token permission test completed!")
        
    except Exception as e:
        print(f"❌ Token test failed: {e}")


if __name__ == "__main__":
    test_token_permissions() 