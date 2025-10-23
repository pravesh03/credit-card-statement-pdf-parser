#!/bin/bash

echo "🚀 Pushing Credit Card Statement Parser to GitHub..."
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Git repository not initialized"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Error: Remote origin not set. Please create the repository on GitHub first:"
    echo "   1. Go to https://github.com/new"
    echo "   2. Repository name: credit-card-statement-parser"
    echo "   3. Description: AI-powered credit card statement parser with FastAPI, React, and multi-issuer support"
    echo "   4. Make it Public"
    echo "   5. DO NOT initialize with README, .gitignore, or license"
    echo "   6. Click 'Create repository'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "📦 Checking repository status..."
git status

echo ""
echo "🔄 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🌐 Repository URL: https://github.com/pravesh03/credit-card-statement-parser"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Visit your repository: https://github.com/pravesh03/credit-card-statement-parser"
    echo "   2. Add topics: fastapi, react, ai, pdf-parser, credit-card, fintech"
    echo "   3. Add a repository description"
    echo "   4. Enable GitHub Pages if you want to host the frontend"
    echo "   5. Consider adding GitHub Actions for CI/CD"
else
    echo ""
    echo "❌ Failed to push to GitHub. Please check:"
    echo "   1. Repository exists at https://github.com/pravesh03/credit-card-statement-parser"
    echo "   2. You have write access to the repository"
    echo "   3. Your GitHub credentials are configured"
fi
