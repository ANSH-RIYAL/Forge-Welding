# The Anvil 🔨

**AI-Powered Project Management & Execution Platform**

Transform ideas into structured, actionable project plans with automated ticket generation and seamless execution workflows. The Anvil bridges the gap between ideation and implementation, creating a complete ecosystem for project management.

## 🎯 Vision: From Ideation to Execution

The Anvil is part of a comprehensive ecosystem that transforms raw ideas into structured, executable projects:

### **Forge** 🔥 (Idea Polishing Tool)
- AI-powered ideation and business plan development
- Structured development of 8 core business considerations
- Collaboration platform for ideators and implementers
- [Learn more about Forge](https://github.com/ANSH-RIYAL/Apocrypha)

### **The Anvil** 🔨 (Project Management Bot)
- Automated GitHub issue generation from YAML implementation plans
- LLM-powered ticket creation and refinement
- Integration with GitHub Projects for visual project management
- Structured workflow from plan to actionable tasks

### **FastMCP** ⚡ (Multi-Tool Framework)
- Custom tool creation and automation
- Hybrid system for ideation-to-execution workflows
- Extensible framework for various use cases
- Seamless integration between planning and implementation

## 🚀 Core Functionality

### **Automated Ticket Generation**
- Parse YAML implementation plans (phases → tasks → subtasks)
- Compare against existing GitHub issues
- Generate missing tickets using LLM prompting
- Post new tickets via GitHub API with proper labeling and milestones

### **Smart Project Management**
- Integration with GitHub Projects (Beta/Next)
- Automatic issue categorization and labeling
- Milestone creation and management
- Dry-run mode for testing and validation

### **LLM-Powered Intelligence**
- Gemini API integration for intelligent ticket generation
- Context-aware descriptions and requirements
- Automatic estimation and complexity assessment
- Smart labeling based on task content and context

## 🎯 Use Cases & Stakeholders

### **Supply Chain Managers & Team Leads**
- **Input**: High-level project requirements and constraints
- **Process**: Discuss project ideas thoroughly with AI assistance
- **Output**: Structured implementation plans ready for technical breakdown

### **Project Managers**
- **Input**: Refined implementation plans and business requirements
- **Process**: Help refine tickets, set priorities, and manage workflows
- **Output**: Organized, prioritized task lists with clear deliverables

### **Engineers & Developers**
- **Input**: Structured tickets with clear requirements and context
- **Process**: Take on tasks with full context and implementation details
- **Output**: Completed features with traceable progress and documentation

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Forge       │    │   The Anvil     │    │    FastMCP      │
│  (Ideation)     │───▶│ (Project Mgmt)  │───▶│  (Execution)    │
│                 │    │                 │    │                 │
│ • AI Ideation   │    │ • YAML Parsing  │    │ • Custom Tools  │
│ • Business Plan │    │ • LLM Tickets   │    │ • Automation    │
│ • Collaboration │    │ • GitHub API    │    │ • Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- GitHub Personal Access Token (with `repo`, `read:org`, `user`, `project` scopes)
- Gemini API Key
- GitHub repository with Projects (Beta/Next) enabled

### Quick Start
```bash
# Clone the repository
git clone https://github.com/ANSH-RIYAL/Forge-Welding.git
cd Forge-Welding

# Install dependencies
pip install -r requirements.txt

# Configure the bot
cp config/config_template.yaml config/config.yaml
# Edit config/config.yaml with your API keys and repository details

# Run the bot
python src/run.py --plan templates/plans/sample_implementation_plan.yaml
```

## 📋 Configuration

### GitHub Setup
1. Create a Personal Access Token with required scopes
2. Enable Projects (Beta/Next) in your repository
3. Note your project ID for configuration

### Gemini API
1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to your configuration file

### Implementation Plans
Create YAML files following this structure:
```yaml
project: "Your Project Name"
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

## 🔧 Usage

### Basic Usage
```bash
# Generate tickets from implementation plan
python src/run.py --plan path/to/implementation_plan.yaml

# Dry run (preview without creating tickets)
python src/run.py --plan path/to/plan.yaml --dry-run

# Include closed issues in comparison
python src/run.py --plan path/to/plan.yaml --include-closed
```

### Advanced Features
- **Automatic Labeling**: Tasks are automatically labeled based on content analysis
- **Milestone Creation**: Phases become GitHub milestones automatically
- **Smart Estimation**: LLM provides complexity estimates for tasks
- **Context Preservation**: Full project context is maintained in ticket descriptions

## 📊 Integration Workflow

### 1. **Ideation Phase** (Forge)
- Stakeholders discuss project requirements
- AI helps develop comprehensive business plans
- Structured output with 8 core considerations

### 2. **Planning Phase** (The Anvil)
- Convert business plans to YAML implementation plans
- Generate structured tickets with full context
- Organize into phases and milestones

### 3. **Execution Phase** (FastMCP)
- Custom tools handle specific implementation needs
- Automated workflows for deployment and testing
- Integration with CI/CD and monitoring systems

## 🎨 Features

### **Intelligent Ticket Generation**
- Context-aware descriptions with full project background
- Automatic labeling based on task content and technology stack
- Smart estimation using LLM analysis
- Proper linking between related tasks and dependencies

### **GitHub Integration**
- Seamless integration with GitHub Issues and Projects
- Automatic milestone creation from phases
- Support for both classic and beta/next projects
- Real-time status tracking and updates

### **Flexible Configuration**
- Dry-run mode for testing and validation
- Configurable ticket limits and filtering
- Customizable prompt templates
- Comprehensive logging and error handling

## 🔒 Security & Best Practices

- Configuration files are gitignored to prevent secret exposure
- API keys are validated before use
- Comprehensive error handling and logging
- Input validation and sanitization
- Secure API communication with GitHub and Gemini

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Create an issue on GitHub for bugs or feature requests
- Check the documentation in `docs/` for detailed usage instructions
- Review the project plan in `PROJECT_PLAN.md` for development roadmap

---

**Built with ❤️ for the project management community**

*The Anvil is part of a larger ecosystem including Forge (ideation) and FastMCP (execution), creating a complete workflow from idea to implementation.* 