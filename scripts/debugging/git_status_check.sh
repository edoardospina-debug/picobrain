#!/bin/bash

# Git Status Check Script for PicoBrain
# Following dev-safeguards.md

echo "=========================================="
echo "PicoBrain Git Status Check"
echo "=========================================="

cd /Users/edo/PyProjects/picobrain

echo -e "\n📍 Current branch:"
git branch --show-current

echo -e "\n📋 Git status:"
git status --short

echo -e "\n📊 Summary:"
if [ -n "$(git status --porcelain)" ]; then
    echo "✓ There are uncommitted changes"
    echo -e "\nDetailed changes:"
    git status
else
    echo "✓ Working directory is clean"
fi

echo -e "\n📤 Unpushed commits:"
git log origin/main..HEAD --oneline 2>/dev/null || echo "No unpushed commits or not on main branch"

echo -e "\n🔍 Recent commits:"
git log --oneline -5
