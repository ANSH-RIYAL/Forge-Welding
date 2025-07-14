"""
Test script for GitHub functionalities
Tests all GitHub API functions independently.
"""

import sys
import os
import json
from typing import Dict, Any

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_manager import load_and_validate_config, get_github_config
from github_client import GitHubClient
from parser import parse_implementation_plan, extract_subtasks_as_dicts


def test_github_connection():
    """Test basic GitHub connection and permissions."""
    print("🔧 Testing GitHub Connection...")
    
    try:
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        # Test connection
        if client.test_connection():
            print("✅ GitHub connection successful")
            
            # Get repository info
            repo_info = client.get_repository_info()
            print(f"📊 Repository: {repo_info.get('full_name', 'Unknown')}")
            print(f"   Open issues: {repo_info.get('open_issues', 0)}")
            print(f"   Stars: {repo_info.get('stars', 0)}")
            print(f"   Language: {repo_info.get('language', 'Unknown')}")
            
            return True
        else:
            print("❌ GitHub connection failed")
            return False
            
    except Exception as e:
        print(f"❌ GitHub connection error: {e}")
        return False


def test_fetch_issues():
    """Test fetching issues from GitHub."""
    print("\n📋 Testing Issue Fetching...")
    
    try:
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        # Fetch open issues
        open_issues = client.fetch_open_issues()
        print(f"✅ Fetched {len(open_issues)} open issues")
        
        # Fetch closed issues
        closed_issues = client.fetch_closed_issues()
        print(f"✅ Fetched {len(closed_issues)} closed issues")
        
        # Show some sample issues
        if open_issues:
            print("\n📝 Sample open issues:")
            for i, issue in enumerate(open_issues[:3], 1):
                print(f"   {i}. #{issue['number']}: {issue['title']}")
                print(f"      Labels: {[label['name'] for label in issue['labels']]}")
                print(f"      State: {issue['state']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Issue fetching error: {e}")
        return False


def test_create_test_issue():
    """Test creating a test issue."""
    print("\n📝 Testing Issue Creation...")
    
    try:
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        # Create a test issue
        test_issue = client.create_issue(
            title="Test Issue - Agentic Bot",
            body="This is a test issue created by the Agentic Project Management Bot for testing purposes.",
            labels=["test", "bot"],
            milestone=None,
            assignees=[]
        )
        
        print(f"✅ Created test issue #{test_issue['number']}")
        print(f"   Title: {test_issue['title']}")
        print(f"   URL: https://github.com/{github_config['repository']}/issues/{test_issue['number']}")
        
        return test_issue['number']
        
    except Exception as e:
        print(f"❌ Issue creation error: {e}")
        return None


def test_update_issue(issue_number: int):
    """Test updating an issue."""
    print(f"\n✏️  Testing Issue Update (Issue #{issue_number})...")
    
    try:
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        # Update the issue
        updated_issue = client.update_issue(
            issue_number=issue_number,
            body="This test issue has been updated by the Agentic Project Management Bot."
        )
        
        if updated_issue:
            print(f"✅ Updated issue #{issue_number}")
            return True
        else:
            print(f"❌ Failed to update issue #{issue_number}")
            return False
            
    except Exception as e:
        print(f"❌ Issue update error: {e}")
        return False


def test_close_issue(issue_number: int):
    """Test closing an issue."""
    print(f"\n🔒 Testing Issue Closure (Issue #{issue_number})...")
    
    try:
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        # Close the issue
        if client.close_issue(issue_number):
            print(f"✅ Closed issue #{issue_number}")
            return True
        else:
            print(f"❌ Failed to close issue #{issue_number}")
            return False
            
    except Exception as e:
        print(f"❌ Issue closure error: {e}")
        return False


def test_search_issues():
    """Test searching for issues."""
    print("\n🔍 Testing Issue Search...")
    
    try:
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        # Search for test issues
        test_issues = client.search_issues_by_title(["test", "Test"])
        print(f"✅ Found {len(test_issues)} issues with 'test' in title")
        
        for issue in test_issues:
            print(f"   #{issue['number']}: {issue['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Issue search error: {e}")
        return False


def test_project_access():
    """Test GitHub project access."""
    print("\n📊 Testing Project Access...")
    
    try:
        config = load_and_validate_config()
        github_config = get_github_config(config)
        
        if not github_config.get('project_id'):
            print("⚠️  No project ID configured, skipping project test")
            return True
        
        client = GitHubClient(
            api_token=github_config['api_token'],
            repository=github_config['repository'],
            project_id=github_config.get('project_id')
        )
        
        project = client.get_project()
        if project:
            print(f"✅ Project access successful: {project.name}")
            return True
        else:
            print("❌ Project access failed")
            return False
            
    except Exception as e:
        print(f"❌ Project access error: {e}")
        return False


def test_implementation_plan_parsing():
    """Test parsing the implementation plan."""
    print("\n📋 Testing Implementation Plan Parsing...")
    
    try:
        config = load_and_validate_config()
        paths_config = config['paths']
        
        # Parse implementation plan
        plan = parse_implementation_plan(paths_config['implementation_plan'])
        
        # Extract subtasks
        subtasks = extract_subtasks_as_dicts(plan)
        
        print(f"✅ Parsed implementation plan successfully")
        print(f"   Project: {plan['project']}")
        print(f"   Phases: {len(plan['phases'])}")
        print(f"   Subtasks: {len(subtasks)}")
        
        # Show some sample subtasks
        print("\n📝 Sample subtasks:")
        for i, subtask in enumerate(subtasks[:3], 1):
            print(f"   {i}. {subtask['name']}")
            print(f"      Phase: {subtask['phase_name']}")
            print(f"      Task: {subtask['task_name']}")
            print(f"      Points: {subtask['estimated_points']}")
            print(f"      Labels: {subtask['labels']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Implementation plan parsing error: {e}")
        return False


def run_all_tests():
    """Run all GitHub functionality tests."""
    print("🧪 Running GitHub Functionality Tests")
    print("=" * 50)
    
    tests = [
        ("GitHub Connection", test_github_connection),
        ("Issue Fetching", test_fetch_issues),
        ("Implementation Plan Parsing", test_implementation_plan_parsing),
        ("Project Access", test_project_access),
        ("Issue Search", test_search_issues),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔧 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Test issue creation/update/closure (optional)
    print("\n🔧 Running: Issue Lifecycle Test")
    try:
        issue_number = test_create_test_issue()
        if issue_number:
            test_update_issue(issue_number)
            test_close_issue(issue_number)
            print("✅ Issue Lifecycle Test: PASSED")
            results.append(("Issue Lifecycle", True))
        else:
            print("❌ Issue Lifecycle Test: FAILED")
            results.append(("Issue Lifecycle", False))
    except Exception as e:
        print(f"❌ Issue Lifecycle Test: ERROR - {e}")
        results.append(("Issue Lifecycle", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! GitHub functionality is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 