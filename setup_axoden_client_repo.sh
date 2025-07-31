#!/bin/bash

# AxoDen Client Repository Setup
# Creates GitHub repository for YalcinkayaE/axoden-client

echo "🚀 Setting up AxoDen Client GitHub Repository"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: Please run this script from the axoden-client directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Initialize git repository
echo "📁 Initializing git repository..."
git init

# Add all files
echo "📋 Adding all files..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: AxoDen Client for Claude Code Integration

Features:
- Complete CLI interface for AI-powered development guidance
- Claude Code integration with clipboard support
- Secure API key management with keyring
- Project analysis and context detection
- Beta user onboarding documentation
- Rich formatting for optimal developer experience

This client enables beta users to:
1. Get AI guidance from AxoDen's proprietary knowledge base
2. Apply recommendations seamlessly in Claude Code workflows
3. Transform reactive problem-solving into systematic approaches

🚀 Generated with AxoDen deployment automation

Co-Authored-By: Claude <noreply@anthropic.com>"

# Set up remote (you'll need to create the GitHub repo first)
echo "🔗 Adding remote repository..."
git remote add origin https://github.com/YalcinkayaE/axoden-client.git

echo ""
echo "📋 Next Steps:"
echo "1. Create repository on GitHub: https://github.com/new"
echo "   - Repository name: axoden-client" 
echo "   - Description: AxoDen Client for Claude Code Integration"
echo "   - Public repository"
echo ""
echo "2. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Update beta user instructions to use the new repository"
echo ""
echo "✅ Repository setup complete!"
echo "📦 Package ready for beta distribution"