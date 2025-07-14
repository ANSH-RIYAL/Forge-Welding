# The Anvil - Agentic Project Management Bot - Project Plan

## 🎯 Project Overview

**Goal**: Create an agentic bot that automatically generates GitHub issues from YAML implementation plans using LLM (Gemini/GPT) for software engineering incubators.

**Core Functionality**: 
- Parse `implementation_plan.yaml` files (phases → tasks → subtasks)
- Compare against existing GitHub issues
- Generate missing tickets using LLM prompting
- Post new tickets via GitHub API
- Integration with GitHub Projects (Beta/Next) for visual project management

## 📋 Development Process (3-Step Approach)

### ✅ Step 1: Design Phase - COMPLETED
- ✅ Created example templates and sample files
- ✅ Defined data models and file structures
- ✅ Established directory organization and naming conventions
- ✅ Designed prompt templates and configuration schema

### ✅ Step 2: Static Files Phase - COMPLETED
- ✅ Created all template files and sample data
- ✅ Established configuration structure
- ✅ Defined prompt templates and ticket schemas
- ✅ Created utility scripts for testing and project management

### 🔄 Step 3: Implementation Phase - IN PROGRESS
- ✅ Core modules implemented (parser.py, llm_planner.py, config_manager.py, run.py)
- ✅ GitHub integration implemented (github_client.py, github_graphql.py)
- ✅ Testing framework established
- ⏳ Project board integration (pending token permissions)
- ⏳ Complete CLI interface refinement

## 🏗️ Finalized System Architecture

### 📁 Complete Repository Structure

```
forge-welding/
├── src/
│   ├── parser.py              # Parse YAML implementation plans
│   ├── llm_planner.py         # LLM integration for ticket generation
│   ├── config_manager.py      # Load and validate configuration
│   ├── github_client.py       # GitHub API integration
│   ├── github_graphql.py      # GitHub GraphQL API for projects
│   └── run.py                 # Main CLI runner
├── templates/
│   ├── prompts/
│   │   └── ticket_generation.yaml  # LLM prompt template
│   └── plans/
│       └── sample_implementation_plan.yaml  # Example implementation plan
├── config/
│   └── config_template.yaml   # Configuration template (gitignored)
├── data/
│   ├── sample_issues.json     # Sample GitHub issues structure
│   └── ticket_templates.json  # Ticket generation templates
├── scripts/                   # Utility and testing scripts
│   ├── manage_project.py      # Project board management
│   ├── check_projects.py      # Project listing utility
│   ├── create_example_tickets.py  # Ticket creation utility
│   ├── create_milestones.py   # Milestone creation utility
│   ├── test_project_board.py  # Project board testing
│   └── test_token_permissions.py  # Token permission testing
├── tests/
│   └── test_github_functions.py  # GitHub integration tests
├── logs/                      # Log files (gitignored)
├── docs/
│   ├── API.md                 # API documentation
│   └── USAGE.md               # Usage instructions
├── requirements.txt           # Python dependencies
├── PROJECT_PLAN.md           # This file
├── README.md                 # Project documentation
└── .gitignore               # Git ignore rules
```

### 🔧 Core Modules Design

| Module | Purpose | Dependencies | Status |
|--------|---------|--------------|--------|
| `parser.py` | Parse YAML plans into structured data | `yaml`, `dataclasses` | ✅ Implemented |
| `llm_planner.py` | Gemini API integration | `google.generativeai` | ✅ Implemented |
| `config_manager.py` | Configuration management | `yaml`, `os` | ✅ Implemented |
| `github_client.py` | GitHub API integration | `requests`, `github` | ✅ Implemented |
| `github_graphql.py` | GitHub GraphQL API for projects | `requests` | ✅ Implemented |
| `run.py` | Main CLI interface | All above modules | ✅ Implemented |

### 📊 Data Models

#### Implementation Plan Structure
```yaml
project: "Project Name"
phases:
  - name: "Phase Name"
    description: "Phase description"
    tasks:
      - name: "Task Name"
        description: "Task description"
        subtasks:
          - name: "Subtask Name"
            description: "Subtask description"
            estimated_points: 3
            labels: ["frontend", "ui"]
```

#### GitHub Issue Structure
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

### 🧠 LLM Integration Design

#### Prompt Template Structure
- **System Prompt**: Defines bot role and constraints
- **User Prompt Template**: Contains implementation plan and existing issues
- **Response Format**: JSON array of GitHub issue objects

#### Gemini API Configuration
- Model: `gemini-1.5-flash`
- Temperature: 0.1 (for consistent output)
- Max tokens: 2048
- Response format: JSON only

### 🔐 Configuration Management

#### Config File Structure (`config.yaml`)
```yaml
gemini:
  api_key: "YOUR_GEMINI_API_KEY_HERE"
  model: "gemini-1.5-flash"
  max_tokens: 2048
  temperature: 0.1

github:
  api_token: "YOUR_GITHUB_TOKEN_HERE"
  repository: "YOUR_GITHUB_USERNAME/YOUR_REPO_NAME"
  project_id: 1  # Set your project ID here
  base_url: "https://api.github.com"

paths:
  implementation_plan: "templates/plans/implementation_plan.yaml"
  prompt_template: "templates/prompts/ticket_generation.yaml"
  log_file: "logs/bot_execution.log"

logging:
  level: "INFO"
  format: "%(asctime)s - %(levelname)s - %(message)s"
  file_mode: "w"

bot:
  dry_run: false
  max_new_tickets: 10
  include_closed_issues: false
```

### 📝 Logging Strategy

#### Log File Structure
- **File**: `logs/bot_execution.log`
- **Mode**: Overwrite on each run (`w`)
- **Format**: `%(asctime)s - %(levelname)s - %(message)s`
- **Level**: INFO

#### Logged Events
- Configuration loading
- Implementation plan parsing
- GitHub issues fetching
- LLM API calls
- Ticket creation results
- Errors and exceptions

### 🔄 Data Flow

1. **Load Configuration** → Parse `config.yaml`
2. **Load Implementation Plan** → Parse YAML plan file
3. **Fetch Existing Issues** → GitHub API call
4. **Compare Plan vs Issues** → Identify missing tickets
5. **Generate New Tickets** → LLM API call
6. **Create GitHub Issues** → GitHub API calls
7. **Log Results** → Write to log file

### 🎯 Functional Scope

#### ✅ In Scope
- Parse YAML implementation plans
- Fetch GitHub issues via API
- Generate missing tickets using Gemini LLM
- Post tickets to GitHub
- CLI interface with error display
- Comprehensive logging
- Configuration management
- Dry-run mode for testing

#### ❌ Out of Scope
- No UI/dashboard
- No user authentication
- No contribution scoring/tracking
- No karma system
- No automatic task reassignment
- No caching or state persistence

## 📋 Next Steps

### Step 2: Static Files Phase - COMPLETED ✅
- ✅ Created sample implementation plan
- ✅ Created prompt templates
- ✅ Created configuration template
- ✅ Created sample data files
- ✅ Created ticket templates
- ✅ Created gitignore rules
- ✅ Created utility scripts for testing and project management

### Step 3: Implementation Phase - IN PROGRESS ✅
- ✅ Core modules implemented (parser.py, llm_planner.py, config_manager.py, run.py)
- ✅ GitHub integration implemented (github_client.py, github_graphql.py)
- ✅ Testing framework established
- ✅ Repository structure organized and cleaned up
- ✅ Configuration template sanitized
- ✅ README.md created with comprehensive documentation

### Next Implementation Tasks:
1. ⏳ Complete project board integration (resolve token permissions)
2. ⏳ Refine CLI interface and error handling
3. ⏳ Add comprehensive unit tests
4. ⏳ Implement dry-run mode improvements
5. ⏳ Add support for custom labels and milestones

## 📝 Implementation Notes

- **LLM Provider**: Gemini API (free tier)
- **Repository**: Configurable via config.yaml
- **GitHub Project**: Configurable via config.yaml
- **Error Display**: All errors shown on terminal
- **Logging**: Overwrite log file on each run
- **Configuration**: Single file with all settings
- **Security**: Config file gitignored, template provided
- **Project Board**: GitHub Projects (Beta/Next) integration
- **Testing**: Comprehensive test suite with utility scripts

---

**Status**: Step 1 Complete, Step 2 Complete, Step 3 In Progress - Core Implementation Complete
**Last Updated**: [Current Date] 