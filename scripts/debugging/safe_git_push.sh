#!/bin/bash

# PicoBrain Safe Git Push Script
# Following dev-safeguards.md procedures

set -e  # Exit on error

echo "=========================================="
echo "🚀 PicoBrain Safe Git Push"
echo "=========================================="

cd /Users/edo/PyProjects/picobrain

# Step 1: Run health check first (as per safeguards)
echo -e "\n📋 Step 1: Running health check..."
if [ -f "./health_check.sh" ]; then
    ./health_check.sh
    if [ $? -ne 0 ]; then
        echo "⚠️  Health check failed! Please fix issues before committing."
        echo "Run ./health_check.sh to see details"
        exit 1
    fi
    echo "✅ Health check passed"
else
    echo "⚠️  health_check.sh not found, skipping health check"
fi

# Step 2: Check current status
echo -e "\n📋 Step 2: Checking git status..."
echo "Current branch: $(git branch --show-current)"

if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Working directory is clean"
    
    # Check for unpushed commits
    unpushed=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
    if [ "$unpushed" -gt 0 ]; then
        echo "📤 Found $unpushed unpushed commits"
        echo -e "\nPushing to remote..."
        git push origin main
        echo "✅ Successfully pushed to GitHub"
    else
        echo "✅ Everything is up to date"
    fi
    exit 0
fi

# Step 3: Show what will be committed
echo -e "\n📋 Files to be committed:"
git status --short

# Step 4: Add all changes
echo -e "\n📋 Step 3: Adding all changes..."
git add -A
echo "✅ All changes staged"

# Step 5: Create commit with descriptive message
echo -e "\n📋 Step 4: Creating commit..."
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
commit_message="feat: save working state - $timestamp

Changes include:
- Claude KB system updates (v2.1)
- Documentation updates
- Script improvements
- Working authentication and employee management
- Health check systems"

git commit -m "$commit_message"
echo "✅ Commit created"

# Step 6: Push to remote
echo -e "\n📋 Step 5: Pushing to GitHub..."
git push origin main
echo "✅ Successfully pushed to GitHub"

# Step 7: Show final status
echo -e "\n📋 Final Status:"
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --oneline)"
echo "Remote: $(git remote -v | grep push | awk '{print $2}')"

echo -e "\n=========================================="
echo "✅ All changes successfully saved to GitHub!"
echo "=========================================="

# Step 8: Update Claude knowledge base
if [ -f "./claude-commit.sh" ]; then
    echo -e "\n📋 Updating Claude knowledge base..."
    ./claude-commit.sh
    echo "✅ Claude knowledge base updated"
fi
