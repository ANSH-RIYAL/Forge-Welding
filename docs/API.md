# Agentic Project Management Bot - API Documentation

## 📋 Module Overview

The bot consists of several core modules that work together to parse implementation plans, generate tickets using LLM, and post them to GitHub.

## 🔧 Core Modules

### 1. `config_manager.py`

**Purpose**: Load and validate configuration from YAML files.

**Main Functions**:
- `load_config(config_path: str) -> dict`: Load configuration from YAML file
- `validate_config(config: dict) -> bool`: Validate required configuration fields
- `get_gemini_config(config: dict) -> dict`: Extract Gemini API configuration
- `get_github_config(config: dict) -> dict`: Extract GitHub API configuration

**Configuration Schema**:
```yaml
gemini:
  api_key: str
  model: str
  max_tokens: int
  temperature: float

github:
  api_token: str
  repository: str
  project_id: int
  base_url: str

paths:
  implementation_plan: str
  prompt_template: str
  log_file: str

logging:
  level: str
  format: str
  file_mode: str

bot:
  dry_run: bool
  max_new_tickets: int
  include_closed_issues: bool
```

### 2. `parser.py`

**Purpose**: Parse YAML implementation plans into structured data.

**Main Functions**:
- `parse_implementation_plan(file_path: str) -> dict`: Parse YAML plan file
- `extract_subtasks(plan: dict) -> list`: Extract all subtasks from plan
- `validate_plan_structure(plan: dict) -> bool`: Validate plan structure

**Data Structures**:
```python
@dataclass
class Subtask:
    name: str
    description: str
    estimated_points: int
    labels: List[str]
    phase_name: str
    task_name: str
```

### 3. `fetch_issues.py`

**Purpose**: Fetch existing GitHub issues via GitHub API.

**Main Functions**:
- `fetch_open_issues(github_config: dict) -> list`: Fetch open issues from repository
- `fetch_closed_issues(github_config: dict) -> list`: Fetch closed issues (optional)
- `parse_issue_data(issues: list) -> list`: Parse GitHub API response

**GitHub API Integration**:
- Uses PyGithub library
- Supports authentication via personal access token
- Handles rate limiting and pagination
- Returns structured issue data

### 4. `llm_planner.py`

**Purpose**: Generate new tickets using Gemini LLM.

**Main Functions**:
- `generate_tickets(plan: dict, existing_issues: list, gemini_config: dict) -> list`: Generate new tickets
- `create_prompt(plan: dict, existing_issues: list) -> str`: Create LLM prompt
- `parse_llm_response(response: str) -> list`: Parse LLM JSON response

**Prompt Structure**:
1. **System Prompt**: Defines bot role and constraints
2. **User Prompt**: Contains implementation plan and existing issues
3. **Response Format**: JSON array of GitHub issue objects

**LLM Configuration**:
- Model: `gemini-1.5-flash`
- Temperature: 0.1 (for consistent output)
- Max tokens: 2048
- Response format: JSON only

### 5. `create_tickets.py`

**Purpose**: Create GitHub issues via GitHub API.

**Main Functions**:
- `create_github_issues(issues: list, github_config: dict) -> list`: Create issues on GitHub
- `validate_issue_data(issue: dict) -> bool`: Validate issue data before creation
- `format_issue_for_github(issue: dict) -> dict`: Format issue for GitHub API

**GitHub Issue Structure**:
```json
{
  "title": "Subtask Name",
  "body": "Detailed description with phase/task context",
  "labels": ["label1", "label2"],
  "milestone": "Phase Name",
  "assignees": [],
  "state": "open"
}
```

### 6. `run.py`

**Purpose**: Main CLI interface and orchestration.

**Main Functions**:
- `main()`: Main entry point
- `setup_logging(config: dict)`: Configure logging
- `run_bot(config: dict)`: Execute the complete bot workflow

**Workflow**:
1. Load configuration
2. Setup logging
3. Parse implementation plan
4. Fetch existing issues
5. Generate new tickets via LLM
6. Create GitHub issues
7. Log results

## 🔄 Data Flow

```
config.yaml → config_manager.py
    ↓
implementation_plan.yaml → parser.py
    ↓
GitHub API → fetch_issues.py
    ↓
plan + issues → llm_planner.py → Gemini API
    ↓
new tickets → create_tickets.py → GitHub API
    ↓
results → logging
```

## 📊 Error Handling

### Configuration Errors
- Missing required fields
- Invalid API keys
- File not found errors

### API Errors
- Network connectivity issues
- Rate limiting
- Authentication failures
- Invalid repository access

### LLM Errors
- Invalid response format
- API quota exceeded
- Model availability issues

### GitHub Errors
- Repository not found
- Insufficient permissions
- Invalid issue data

## 🧪 Testing

### Unit Tests
- `test_config_manager.py`: Configuration loading and validation
- `test_parser.py`: YAML parsing and validation
- `test_fetch_issues.py`: GitHub API integration
- `test_llm_planner.py`: LLM integration
- `test_create_tickets.py`: GitHub issue creation

### Integration Tests
- `test_end_to_end.py`: Complete workflow testing
- `test_error_handling.py`: Error scenario testing

## 📝 Logging

### Log Levels
- `DEBUG`: Detailed execution information
- `INFO`: General execution flow
- `WARNING`: Non-critical issues
- `ERROR`: Critical errors

### Log Format
```
%(asctime)s - %(levelname)s - %(message)s
```

### Log File
- Location: `logs/bot_execution.log`
- Mode: Overwrite on each run (`w`)
- Rotation: Manual (new file each run)

## 🔒 Security Considerations

### API Keys
- Stored in `config.yaml` (gitignored)
- Never logged or displayed
- Validated on startup

### GitHub Permissions
- Requires `repo` scope for private repositories
- Requires `public_repo` scope for public repositories
- Token should have appropriate permissions

### Data Handling
- No sensitive data stored permanently
- All data processed in memory
- Logs contain no sensitive information 