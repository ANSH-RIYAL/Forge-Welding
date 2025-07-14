# Agentic Project Management Bot - Project Plan

## 🎯 Project Overview

**Goal**: Create an agentic bot that automatically generates GitHub issues from YAML implementation plans using LLM (Gemini/GPT) for software engineering incubators.

**Core Functionality**: 
- Parse `implementation_plan.yaml` files (phases → tasks → subtasks)
- Compare against existing GitHub issues
- Generate missing tickets using LLM prompting
- Post new tickets via GitHub API

## 📋 Development Process (3-Step Approach)

### ✅ Step 1: Design Phase - COMPLETED
- ✅ Created example templates and sample files
- ✅ Defined data models and file structures
- ✅ Established directory organization and naming conventions
- ✅ Designed prompt templates and configuration schema

### 🔄 Step 2: Static Files Phase - IN PROGRESS
- ✅ Created all template files and sample data
- ✅ Established configuration structure
- ✅ Defined prompt templates and ticket schemas

### ⏳ Step 3: Implementation Phase - PENDING
- Build the actual implementation based on the design and static files

## 🏗️ Finalized System Architecture

### 📁 Complete Repository Structure

```
forge-welding/
├── src/
│   ├── parser.py              # Parse YAML implementation plans
│   ├── fetch_issues.py        # Fetch GitHub issues via API
│   ├── llm_planner.py         # LLM integration for ticket generation
│   ├── create_tickets.py      # Post tickets to GitHub
│   ├── config_manager.py      # Load and validate configuration
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
├── logs/                      # Log files (gitignored)
├── docs/
│   ├── API.md                 # API documentation
│   └── USAGE.md               # Usage instructions
├── tests/
│   └── test_*.py             # Unit tests
├── requirements.txt           # Python dependencies
├── PROJECT_PLAN.md           # This file
└── .gitignore               # Git ignore rules
```

### 🔧 Core Modules Design

| Module | Purpose | Dependencies |
|--------|---------|--------------|
| `parser.py` | Parse YAML plans into structured data | `yaml`, `dataclasses` |
| `fetch_issues.py` | GitHub API integration | `requests`, `github` |
| `llm_planner.py` | Gemini API integration | `google.generativeai` |
| `create_tickets.py` | Create GitHub issues | `requests`, `github` |
| `config_manager.py` | Configuration management | `yaml`, `os` |
| `run.py` | Main CLI interface | All above modules |

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
  api_key: "YOUR_GEMINI_API_KEY"
  model: "gemini-1.5-flash"
  max_tokens: 2048
  temperature: 0.1

github:
  api_token: "YOUR_GITHUB_TOKEN"
  repository: "ANSH-RIYAL/Test-run"
  project_id: 3
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

### Step 3: Implementation Phase - READY TO START
1. Create Python source files (`src/`)
2. Implement configuration management
3. Implement YAML parser
4. Implement GitHub API integration
5. Implement Gemini LLM integration
6. Implement main CLI runner
7. Add error handling and logging
8. Create tests

## 📝 Implementation Notes

- **LLM Provider**: Gemini API (free tier)
- **Repository**: `ANSH-RIYAL/Test-run`
- **GitHub Project**: ID 3
- **Error Display**: All errors shown on terminal
- **Logging**: Overwrite log file on each run
- **Configuration**: Single file with all settings
- **Security**: Config file gitignored, template provided

---

**Status**: Step 1 Complete, Step 2 Complete, Ready for Step 3 - Implementation
**Last Updated**: [Current Date] 