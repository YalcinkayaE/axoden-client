# AxoDen Client - Claude Code Integration

Transform your development workflow with AI-powered methodology recommendations from AxoDen's proprietary knowledge base, seamlessly integrated with Claude Code.

## 🚀 Quick Start

### Installation

```bash
pip install axoden-client
```

### First-Time Setup

```bash
# Easy API key setup (recommended)
axoden setup-key

# Or run full interactive setup
axoden quickstart

# Or use environment variable (best for automation)
export AXODEN_API_KEY='your_beta_api_key'
axoden config --test
```

### Basic Usage

```bash
# Get methodology recommendation
axoden recommend "debug memory leak in production API"

# Analyze current project
axoden analyze

# List available methodologies
axoden list
```

## 🎯 Claude Code Integration Workflow

### Method 1: Direct CLI Usage

1. **Get Recommendation**
   ```bash
   axoden recommend "optimize database queries"
   ```

2. **Copy the formatted output** and paste into Claude Code

3. **Ask Claude Code** to implement using the recommended methodology

### Method 2: Clipboard Integration

```bash
# Automatically copies methodology prompt to clipboard
python -m axoden_client.claude_integration "fix flaky test failures"
```

Then paste directly into Claude Code!

### Method 3: File-Based Workflow

```bash
# Save recommendation to file
axoden recommend "implement caching strategy" --save

# Creates: axoden_recommendation_20240131_143022.md
```

Reference the file in your Claude Code session.

## 📚 Example Workflows

### Debugging Workflow
```bash
# 1. Get debugging methodology
axoden recommend "debug intermittent API timeout errors"

# 2. AxoDen returns systematic debugging approach
# 3. Apply in Claude Code: "Using the Test Isolation methodology, help me debug..."
```

### Architecture Decisions
```bash
# 1. Get architecture methodology
axoden recommend "design microservices architecture" --context '{"team_size": 5}'

# 2. Receive Domain-Driven Design methodology
# 3. Apply: "Following DDD principles from AxoDen, design a service architecture..."
```

### Performance Optimization
```bash
# 1. Analyze project for performance recommendations
axoden analyze --path ./src

# 2. Get targeted optimization methodologies
# 3. Implement with Claude Code guidance
```

## 🔧 Advanced Configuration

### API Key Setup Options

**Option 1: Easy Setup (Recommended)**
```bash
axoden setup-key  # Interactive setup with clipboard support
```

**Option 2: Environment Variable**
```bash
export AXODEN_API_KEY="your_api_key"
axoden config --test
```

**Option 3: Direct Configuration**
```bash
axoden config --api-key YOUR_API_KEY
```

**Advanced Configuration**
```bash
export AXODEN_API_URL="https://api.axoden.com"  # For custom deployments
export AXODEN_AGENT_ID="custom-agent-id"  # Optional
```

### Configuration File
```bash
# Show current config
axoden config --show

# Test API connection
axoden config --test

# Reset configuration
rm -rf ~/.axoden
```

## 🎨 Output Formats

### Claude Code Optimized (Default)
```bash
axoden recommend "implement authentication" --format claude
```
Returns formatted markdown with:
- Clear methodology name and confidence
- Step-by-step implementation guide
- Reasoning and alternatives
- Ready to paste into Claude Code

### JSON Format
```bash
axoden recommend "implement authentication" --format json
```
Returns structured data for programmatic use.

## 🤝 Beta Testing Guide

As a beta tester, please help us improve by:

1. **Testing Various Problems**
   - Try different types of development challenges
   - Test with different project contexts
   - Verify methodology relevance

2. **Integration Feedback**
   - How well do recommendations work with Claude Code?
   - Is the workflow smooth?
   - What features are missing?

3. **Report Issues**
   ```bash
   # Include version info when reporting
   axoden --version
   ```

## 🔍 Troubleshooting

### Authentication Issues
```bash
# Verify API key is set
axoden config --show

# Test connection
axoden config --test

# Re-enter API key
axoden config --api-key YOUR_KEY
```

### No Recommendations Returned
- Check API connection: `curl https://api.axoden.com/health`
- Verify methodology brain is active and responding
- Try simpler problem descriptions

### Clipboard Not Working
- macOS: Requires `pbcopy` (built-in)
- Linux: Install `xclip`: `sudo apt-get install xclip`
- Windows: Requires PowerShell (built-in)

## 📊 How It Works

1. **Problem Analysis**: AxoDen analyzes your development challenge
2. **Methodology Matching**: Searches proprietary knowledge base across multiple domains
3. **Cognitive Optimization**: Matches recommendations to developer thinking style
4. **Claude Code Format**: Formats guidance for optimal Claude Code consumption
5. **Seamless Integration**: Apply methodologies directly in your workflow

## 🚀 Coming Soon

- [ ] VS Code extension for inline methodology suggestions
- [ ] Claude Code plugin for automatic methodology lookup
- [ ] Team collaboration features
- [ ] Methodology success tracking
- [ ] Custom methodology creation

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

This is a beta release. Please report issues and suggestions at:
https://github.com/YalcinkayaE/axoden-client/issues

## 📧 Support

- Email: support@axoden.com
- Documentation: https://docs.axoden.com
- API Status: https://status.axoden.com

---

**AxoDen Client v0.1.0** - Empowering developers with proven methodologies