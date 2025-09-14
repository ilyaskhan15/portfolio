#!/bin/bash

# Git Setup Script for Django Portfolio Blog
echo "🚀 Setting up Git repository for Django Portfolio Blog..."

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first:"
    echo "   Ubuntu/Debian: sudo apt-get install git"
    echo "   macOS: brew install git"
    echo "   Windows: Download from https://git-scm.com/"
    exit 1
fi

# Check if already a Git repository
if [ -d ".git" ]; then
    echo "✅ Git repository already initialized."
    echo "Current status:"
    git status --short
    exit 0
fi

# Initialize Git repository
echo "📁 Initializing Git repository..."
git init

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo "❌ .gitignore file not found. Please ensure .gitignore exists."
    exit 1
fi

# Add all files
echo "📂 Adding all files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Django Portfolio Blog project

- Django 5.1.1 with modular settings
- Portfolio and Blog applications
- Production-ready configuration for Render.com
- PostgreSQL database support
- Tailwind CSS responsive design
- CKEditor for rich content management
- REST API with Django REST Framework"

echo ""
echo "✅ Git repository successfully initialized!"
echo ""
echo "🔗 Next steps for GitHub setup:"
echo "1. Create a new repository on GitHub.com"
echo "2. Run these commands (replace YOUR_USERNAME and REPO_NAME):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Follow DEPLOYMENT.md for Render.com deployment instructions"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"