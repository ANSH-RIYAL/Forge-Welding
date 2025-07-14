# Agentic Project Management Bot - Usage Guide

## 🚀 Quick Start

### 1. Setup Configuration

1. Copy the configuration template:
   ```bash
   cp config/config_template.yaml config/config.yaml
   ```

2. Edit `config/config.yaml` with your actual API keys:
   ```yaml
   gemini:
     api_key: "YOUR_ACTUAL_GEMINI_API_KEY"
   
   github:
     api_token: "YOUR_ACTUAL_GITHUB_TOKEN"
   ```

### 2. Create Implementation Plan

Create your implementation plan in YAML format:
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

### 3. Run the Bot

```bash
python src/run.py
```

## 📋 Configuration Options

### Gemini API Settings
- `api_key`: Your Gemini API key
- `model`: LLM model to use (default: "gemini-1.5-flash")
- `max_tokens`: Maximum response length (default: 2048)
- `temperature`: Response randomness (default: 0.1)

### GitHub Settings
- `api_token`: Your GitHub personal access token
- `repository`: Repository in format "owner/repo"
- `project_id`: GitHub project ID (if using projects)
- `base_url`: GitHub API base URL

### Bot Behavior
- `dry_run`: Set to `true` to see what would be created without actually creating tickets
- `max_new_tickets`: Maximum tickets to create in one run
- `include_closed_issues`: Whether to consider closed issues when checking for duplicates

## 📁 File Structure

```
forge-welding/
├── config/config.yaml          # Your configuration (create from template)
├── templates/plans/            # Your implementation plans
├── logs/                      # Execution logs
└── src/                       # Source code
```

## 🔧 Advanced Usage

### Dry Run Mode
Test the bot without creating actual tickets:
```bash
# Edit config.yaml to set dry_run: true
python src/run.py
```

### Custom Implementation Plan
Use a different implementation plan:
```bash
# Edit config.yaml to change the path
paths:
  implementation_plan: "path/to/your/plan.yaml"
```

### Logging
Check execution logs:
```bash
cat logs/bot_execution.log
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your Gemini API key is valid
   - Check your GitHub token has appropriate permissions

2. **Repository Access**
   - Verify your GitHub token has access to the repository
   - Check repository name format: "owner/repo"

3. **YAML Parsing Errors**
   - Validate your implementation plan YAML syntax
   - Use a YAML validator to check format

4. **Network Issues**
   - Check internet connectivity
   - Verify API endpoints are accessible

### Debug Mode
Enable verbose logging by editing `config.yaml`:
```yaml
logging:
  level: "DEBUG"
```

## 📝 Example Implementation Plan

See `templates/plans/sample_implementation_plan.yaml` for a complete example.

## 🔒 Security Notes

- Never commit your `config.yaml` file (it's gitignored)
- Keep your API keys secure
- Use environment variables for production deployments
- Regularly rotate your GitHub tokens

## 📞 Support

For issues or questions:
1. Check the logs in `logs/bot_execution.log`
2. Verify your configuration in `config/config.yaml`
3. Test with dry-run mode first 