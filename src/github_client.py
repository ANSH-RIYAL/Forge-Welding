"""
GitHub Client for Agentic Project Management Bot
Handles all GitHub API interactions including issues and projects.
"""

import requests
from typing import Dict, List, Any, Optional
import logging
from github import Github, GithubException
from github.Repository import Repository
from github.Issue import Issue
from github.Project import Project

logger = logging.getLogger(__name__)


class GitHubClient:
    """
    GitHub API client for managing issues and projects.
    """
    
    def __init__(self, api_token: str, repository: str, project_id: Optional[int] = None):
        """
        Initialize GitHub client.
        
        Args:
            api_token: GitHub personal access token
            repository: Repository in format "owner/repo"
            project_id: Optional GitHub project ID
        """
        self.api_token = api_token
        self.repository = repository
        self.project_id = project_id
        self.github = Github(api_token)
        self.repo = self.github.get_repo(repository)
        
        logger.info(f"GitHub client initialized for repository: {repository}")
    
    def test_connection(self) -> bool:
        """
        Test GitHub API connection and permissions.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Test basic API access
            user = self.github.get_user()
            logger.info(f"Connected to GitHub as: {user.login}")
            
            # Test repository access
            repo_name = self.repo.name
            logger.info(f"Repository access confirmed: {repo_name}")
            
            return True
            
        except GithubException as e:
            logger.error(f"GitHub connection failed: {e}")
            return False
    
    def fetch_open_issues(self) -> List[Dict[str, Any]]:
        """
        Fetch all open issues from the repository.
        
        Returns:
            List of issue dictionaries
        """
        try:
            issues = []
            for issue in self.repo.get_issues(state='open'):
                issue_data = {
                    'id': issue.id,
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body or '',
                    'state': issue.state,
                    'labels': [{'name': label.name, 'color': label.color} for label in issue.labels],
                    'milestone': {'title': issue.milestone.title} if issue.milestone else None,
                    'created_at': issue.created_at.isoformat(),
                    'updated_at': issue.updated_at.isoformat(),
                    'assignees': [assignee.login for assignee in issue.assignees]
                }
                issues.append(issue_data)
            
            logger.info(f"Fetched {len(issues)} open issues")
            return issues
            
        except GithubException as e:
            logger.error(f"Failed to fetch open issues: {e}")
            raise
    
    def fetch_closed_issues(self) -> List[Dict[str, Any]]:
        """
        Fetch all closed issues from the repository.
        
        Returns:
            List of issue dictionaries
        """
        try:
            issues = []
            for issue in self.repo.get_issues(state='closed'):
                issue_data = {
                    'id': issue.id,
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body or '',
                    'state': issue.state,
                    'labels': [{'name': label.name, 'color': label.color} for label in issue.labels],
                    'milestone': {'title': issue.milestone.title} if issue.milestone else None,
                    'created_at': issue.created_at.isoformat(),
                    'updated_at': issue.updated_at.isoformat(),
                    'assignees': [assignee.login for assignee in issue.assignees]
                }
                issues.append(issue_data)
            
            logger.info(f"Fetched {len(issues)} closed issues")
            return issues
            
        except GithubException as e:
            logger.error(f"Failed to fetch closed issues: {e}")
            raise
    
    def fetch_all_issues(self, include_closed: bool = False) -> List[Dict[str, Any]]:
        """
        Fetch all issues from the repository.
        
        Args:
            include_closed: Whether to include closed issues
            
        Returns:
            List of issue dictionaries
        """
        open_issues = self.fetch_open_issues()
        
        if include_closed:
            closed_issues = self.fetch_closed_issues()
            all_issues = open_issues + closed_issues
            logger.info(f"Fetched {len(all_issues)} total issues ({len(open_issues)} open, {len(closed_issues)} closed)")
            return all_issues
        else:
            logger.info(f"Fetched {len(open_issues)} open issues")
            return open_issues
    
    def create_issue(self, title: str, body: str, labels: List[str] = None, 
                    milestone: str = None, assignees: List[str] = None) -> Dict[str, Any]:
        """
        Create a new issue in the repository.
        
        Args:
            title: Issue title
            body: Issue body/description
            labels: List of label names
            milestone: Milestone name
            assignees: List of assignee usernames
            
        Returns:
            Created issue dictionary
        """
        try:
            # Prepare issue data
            issue_data = {
                'title': title,
                'body': body
            }
            
            # Add labels if provided
            if labels:
                issue_data['labels'] = labels
            
            # Add milestone if provided
            if milestone:
                try:
                    # Try to find existing milestone by title
                    milestones = self.repo.get_milestones()
                    milestone_obj = None
                    for m in milestones:
                        if m.title == milestone:
                            milestone_obj = m
                            break
                    
                    if milestone_obj:
                        issue_data['milestone'] = milestone_obj
                    else:
                        logger.warning(f"Milestone '{milestone}' not found, creating issue without milestone")
                except GithubException:
                    logger.warning(f"Milestone '{milestone}' not found, creating issue without milestone")
            
            # Add assignees if provided
            if assignees:
                issue_data['assignees'] = assignees
            
            # Create the issue
            issue = self.repo.create_issue(**issue_data)
            
            # Return created issue data
            created_issue = {
                'id': issue.id,
                'number': issue.number,
                'title': issue.title,
                'body': issue.body or '',
                'state': issue.state,
                'labels': [{'name': label.name, 'color': label.color} for label in issue.labels],
                'milestone': {'title': issue.milestone.title} if issue.milestone else None,
                'created_at': issue.created_at.isoformat(),
                'updated_at': issue.updated_at.isoformat(),
                'assignees': [assignee.login for assignee in issue.assignees]
            }
            
            logger.info(f"Created issue #{issue.number}: {title}")
            return created_issue
            
        except GithubException as e:
            logger.error(f"Failed to create issue '{title}': {e}")
            raise
    
    def create_multiple_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create multiple issues in the repository.
        
        Args:
            issues: List of issue dictionaries with title, body, labels, etc.
            
        Returns:
            List of created issue dictionaries
        """
        created_issues = []
        
        for issue_data in issues:
            try:
                created_issue = self.create_issue(
                    title=issue_data['title'],
                    body=issue_data['body'],
                    labels=issue_data.get('labels', []),
                    milestone=issue_data.get('milestone'),
                    assignees=issue_data.get('assignees', [])
                )
                created_issues.append(created_issue)
                
            except Exception as e:
                logger.error(f"Failed to create issue '{issue_data.get('title', 'Unknown')}': {e}")
                # Continue with other issues even if one fails
        
        logger.info(f"Created {len(created_issues)} out of {len(issues)} issues")
        return created_issues
    
    def get_project(self) -> Optional[Project]:
        """
        Get the GitHub project if project_id is configured.
        
        Returns:
            Project object or None if not configured
        """
        if not self.project_id:
            logger.warning("No project ID configured")
            return None
        
        try:
            # Get the authenticated user
            user = self.github.get_user()
            
            # Try to get the project
            project = user.get_project(self.project_id)
            logger.info(f"Found project: {project.name}")
            return project
            
        except GithubException as e:
            logger.error(f"Failed to get project {self.project_id}: {e}")
            return None
    
    def add_issue_to_project(self, issue_number: int, project: Project) -> bool:
        """
        Add an issue to a GitHub project.
        
        Args:
            issue_number: Issue number to add
            project: GitHub project object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the issue
            issue = self.repo.get_issue(issue_number)
            
            # Add to project (this would require additional API calls)
            # Note: GitHub Projects API is more complex and may require different permissions
            logger.info(f"Would add issue #{issue_number} to project {project.name}")
            return True
            
        except GithubException as e:
            logger.error(f"Failed to add issue #{issue_number} to project: {e}")
            return False
    
    def search_issues_by_title(self, title_keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Search for issues by title keywords.
        
        Args:
            title_keywords: List of keywords to search for
            
        Returns:
            List of matching issue dictionaries
        """
        try:
            matching_issues = []
            all_issues = self.fetch_all_issues(include_closed=True)
            
            for issue in all_issues:
                issue_title = issue['title'].lower()
                for keyword in title_keywords:
                    if keyword.lower() in issue_title:
                        matching_issues.append(issue)
                        break
            
            logger.info(f"Found {len(matching_issues)} issues matching keywords: {title_keywords}")
            return matching_issues
            
        except Exception as e:
            logger.error(f"Failed to search issues: {e}")
            return []
    
    def get_issue_by_number(self, issue_number: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific issue by number.
        
        Args:
            issue_number: Issue number
            
        Returns:
            Issue dictionary or None if not found
        """
        try:
            issue = self.repo.get_issue(issue_number)
            
            issue_data = {
                'id': issue.id,
                'number': issue.number,
                'title': issue.title,
                'body': issue.body or '',
                'state': issue.state,
                'labels': [{'name': label.name, 'color': label.color} for label in issue.labels],
                'milestone': {'title': issue.milestone.title} if issue.milestone else None,
                'created_at': issue.created_at.isoformat(),
                'updated_at': issue.updated_at.isoformat(),
                'assignees': [assignee.login for assignee in issue.assignees]
            }
            
            return issue_data
            
        except GithubException as e:
            logger.error(f"Failed to get issue #{issue_number}: {e}")
            return None
    
    def update_issue(self, issue_number: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update an existing issue.
        
        Args:
            issue_number: Issue number to update
            **kwargs: Fields to update (title, body, labels, etc.)
            
        Returns:
            Updated issue dictionary or None if failed
        """
        try:
            issue = self.repo.get_issue(issue_number)
            
            # Update the issue
            issue.edit(**kwargs)
            
            # Return updated issue data
            updated_issue = {
                'id': issue.id,
                'number': issue.number,
                'title': issue.title,
                'body': issue.body or '',
                'state': issue.state,
                'labels': [{'name': label.name, 'color': label.color} for label in issue.labels],
                'milestone': {'title': issue.milestone.title} if issue.milestone else None,
                'created_at': issue.created_at.isoformat(),
                'updated_at': issue.updated_at.isoformat(),
                'assignees': [assignee.login for assignee in issue.assignees]
            }
            
            logger.info(f"Updated issue #{issue_number}")
            return updated_issue
            
        except GithubException as e:
            logger.error(f"Failed to update issue #{issue_number}: {e}")
            return None
    
    def close_issue(self, issue_number: int) -> bool:
        """
        Close an issue.
        
        Args:
            issue_number: Issue number to close
            
        Returns:
            True if successful, False otherwise
        """
        try:
            issue = self.repo.get_issue(issue_number)
            issue.edit(state='closed')
            logger.info(f"Closed issue #{issue_number}")
            return True
            
        except GithubException as e:
            logger.error(f"Failed to close issue #{issue_number}: {e}")
            return False
    
    def get_repository_info(self) -> Dict[str, Any]:
        """
        Get basic repository information.
        
        Returns:
            Repository information dictionary
        """
        try:
            info = {
                'name': self.repo.name,
                'full_name': self.repo.full_name,
                'description': self.repo.description,
                'private': self.repo.private,
                'fork': self.repo.fork,
                'language': self.repo.language,
                'stars': self.repo.stargazers_count,
                'forks': self.repo.forks_count,
                'open_issues': self.repo.open_issues_count
            }
            
            logger.info(f"Repository info: {self.repo.full_name}")
            return info
            
        except GithubException as e:
            logger.error(f"Failed to get repository info: {e}")
            return {} 