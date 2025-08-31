#!/bin/bash

# Backup current state before making any changes
echo "📦 Creating backup of current state..."
mkdir -p ../picobrain-backups
timestamp=$(date +%Y%m%d_%H%M%S)
tar -czf ../picobrain-backups/frontend_backup_${timestamp}.tar.gz frontend/

echo "✅ Backup created: ../picobrain-backups/frontend_backup_${timestamp}.tar.gz"

# Check git status
echo ""
echo "📊 Current git status:"
git status --short

echo ""
echo "📝 Recent commits:"
git log --oneline -10

echo ""
echo "🔍 Files changed in the last commit:"
git diff --name-only HEAD~1

echo ""
echo "To revert the last commit (if needed):"
echo "  git revert HEAD"
echo ""
echo "To reset to a specific commit:"
echo "  git reset --hard <commit-hash>"
echo ""
echo "To view changes in detail:"
echo "  git diff HEAD~1"
