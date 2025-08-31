#!/bin/bash

# Quick Git Operations for PicoBrain

cd /Users/edo/PyProjects/picobrain

case "$1" in
    status)
        echo "📍 Current branch: $(git branch --show-current)"
        echo -e "\n📋 Git status:"
        git status
        echo -e "\n📤 Unpushed commits:"
        git log origin/main..HEAD --oneline 2>/dev/null || echo "None"
        ;;
    
    add)
        echo "📋 Adding all changes..."
        git add -A
        git status --short
        echo "✅ All changes staged"
        ;;
    
    commit)
        if [ -z "$2" ]; then
            message="feat: save working state - $(date +"%Y-%m-%d %H:%M:%S")"
        else
            message="$2"
        fi
        echo "📋 Creating commit: $message"
        git commit -m "$message"
        echo "✅ Commit created"
        ;;
    
    push)
        echo "📤 Pushing to GitHub..."
        git push origin main
        echo "✅ Pushed successfully"
        ;;
    
    all)
        # Do everything in sequence
        echo "🚀 Running complete git save workflow..."
        
        # Add all changes
        echo -e "\n📋 Adding all changes..."
        git add -A
        
        # Show what's being committed
        echo -e "\n📋 Changes to commit:"
        git status --short
        
        # Commit with timestamp
        message="feat: save working state - $(date +"%Y-%m-%d %H:%M:%S")

Includes:
- Claude KB v2.1 system
- Working authentication
- Employee management
- Documentation updates"
        
        echo -e "\n📋 Creating commit..."
        git commit -m "$message" || echo "No changes to commit"
        
        # Push to remote
        echo -e "\n📤 Pushing to GitHub..."
        git push origin main
        
        echo -e "\n✅ All done!"
        ;;
    
    *)
        echo "Usage: $0 {status|add|commit|push|all}"
        echo "  status - Show git status"
        echo "  add    - Stage all changes"
        echo "  commit [message] - Create commit"
        echo "  push   - Push to GitHub"
        echo "  all    - Do everything (add, commit, push)"
        ;;
esac
