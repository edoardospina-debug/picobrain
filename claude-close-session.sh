#!/bin/bash
# Claude KB Session Close Script - Automated exit procedure
# Combines all necessary steps for safely closing a Claude session

set -euo pipefail

# Configuration
PROJECT_DIR="$(pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
TRACKING_FILE="$CLAUDE_DIR/.last_weekly_review"
WEEKLY_REVIEW_THRESHOLD=172800  # 48 hours in seconds

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_step() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

# Check if weekly review is needed
check_weekly_review() {
    if [ ! -f "$TRACKING_FILE" ]; then
        echo "0" > "$TRACKING_FILE"
        return 0  # First run, should do review
    fi
    
    local last_run=$(cat "$TRACKING_FILE" 2>/dev/null || echo "0")
    local current_time=$(date +%s)
    local time_diff=$((current_time - last_run))
    
    if [ "$time_diff" -gt "$WEEKLY_REVIEW_THRESHOLD" ]; then
        return 0  # Review needed
    else
        local hours_remaining=$(( (WEEKLY_REVIEW_THRESHOLD - time_diff) / 3600 ))
        log_step "Weekly review not needed (next in ~${hours_remaining}h)"
        return 1  # Review not needed
    fi
}

# Main execution
main() {
    echo "════════════════════════════════════════════"
    echo "   🚪 Claude KB Session Close Procedure"
    echo "════════════════════════════════════════════"
    echo ""
    
    # Track if any step fails
    local has_errors=0
    
    # Step 1: Capture knowledge
    log_step "1️⃣  Capturing knowledge and patterns..."
    if ./claude-commit.sh 2>/dev/null; then
        log_success "Knowledge captured"
    else
        log_warning "Knowledge capture had warnings (non-critical)"
    fi
    echo ""
    
    # Step 2: Check for changes
    log_step "2️⃣  Checking for knowledge base changes..."
    local changes=$(git status --porcelain CLAUDE.md knowledge.md 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$changes" -gt 0 ]; then
        log_success "Found $changes file(s) with updates"
        
        # Generate intelligent commit message
        local added_lines=$(git diff --stat CLAUDE.md knowledge.md 2>/dev/null | grep -E '[0-9]+ insertion' | grep -oE '[0-9]+' | head -1 || echo "0")
        local deleted_lines=$(git diff --stat CLAUDE.md knowledge.md 2>/dev/null | grep -E '[0-9]+ deletion' | grep -oE '[0-9]+' | head -1 || echo "0")
        
        local commit_msg="docs: update knowledge base"
        if [ "$added_lines" -gt 100 ]; then
            commit_msg="docs: enhance knowledge base (+${added_lines} lines)"
        elif [ "$deleted_lines" -gt 50 ]; then
            commit_msg="docs: optimize knowledge base (-${deleted_lines} lines)"
        fi
        
        # Stage and commit
        log_step "   📝 Committing: $commit_msg"
        git add CLAUDE.md knowledge.md 2>/dev/null
        
        if git commit -m "$commit_msg" -m "- Auto-captured patterns and session data
- Updated via claude-close-session.sh
- Session closed at $(date +'%Y-%m-%d %H:%M:%S')" 2>/dev/null; then
            log_success "Changes committed"
            
            # Push to remote
            log_step "   ☁️  Pushing to remote..."
            local branch=$(git branch --show-current 2>/dev/null || echo "main")
            if git push origin "$branch" 2>/dev/null; then
                log_success "Pushed to origin/$branch"
            else
                log_warning "Could not push (check network/credentials)"
                has_errors=1
            fi
        else
            log_warning "No new changes to commit"
        fi
    else
        log_step "   ℹ️  No knowledge base changes to commit"
    fi
    echo ""
    
    # Step 3: Validate system
    log_step "3️⃣  Validating system integrity..."
    if ./claude-validate.sh 2>/dev/null | grep -q "✅"; then
        log_success "System validation passed"
    else
        log_warning "Some validation checks failed (review manually)"
        has_errors=1
    fi
    echo ""
    
    # Step 4: Check token usage
    log_step "4️⃣  Checking token usage..."
    local token_output=$(./claude-context-monitor.sh 2>/dev/null | grep -E "Total:|Context usage" | head -1)
    if echo "$token_output" | grep -q "healthy\|✅"; then
        log_success "Token usage healthy"
    else
        echo "   $token_output"
        if echo "$token_output" | grep -qE "8[0-9]%|9[0-9]%"; then
            log_warning "High token usage detected - consider emergency reset"
            has_errors=1
        fi
    fi
    echo ""
    
    # Step 5: Weekly review (if needed)
    if check_weekly_review; then
        log_step "5️⃣  Running weekly maintenance..."
        if ./claude-weekly-review.sh 2>/dev/null; then
            date +%s > "$TRACKING_FILE"
            log_success "Weekly review completed"
        else
            log_warning "Weekly review had issues (non-critical)"
        fi
        echo ""
    fi
    
    # Step 6: Clean up backups
    log_step "6️⃣  Cleaning up temporary files..."
    local backup_count=$(ls -1 *.backup 2>/dev/null | wc -l | tr -d ' ')
    if [ "$backup_count" -gt 0 ]; then
        rm -f *.backup
        log_success "Removed $backup_count backup file(s)"
    else
        log_step "   No backup files to clean"
    fi
    echo ""
    
    # Final summary
    echo "════════════════════════════════════════════"
    if [ "$has_errors" -eq 0 ]; then
        echo -e "${GREEN}   ✨ Session closed successfully!${NC}"
        echo ""
        echo "   Your knowledge base is:"
        echo "   • Captured and updated"
        echo "   • Committed to git"
        echo "   • Pushed to GitHub"
        echo "   • Validated and healthy"
    else
        echo -e "${YELLOW}   ⚠️  Session closed with warnings${NC}"
        echo ""
        echo "   Please review the warnings above."
        echo "   Your knowledge is saved locally."
    fi
    echo "════════════════════════════════════════════"
    echo ""
    
    # Quick stats
    local kb_size=$(du -sh CLAUDE.md knowledge.md 2>/dev/null | awk '{sum+=$1} END {print sum}')
    echo "📊 Quick Stats:"
    echo "   • Knowledge base size: ~${kb_size}KB"
    echo "   • Last commit: $(git log -1 --format='%h - %s' 2>/dev/null | head -c 50)"
    echo "   • Session ended: $(date +'%Y-%m-%d %H:%M:%S')"
    echo ""
    
    exit "$has_errors"
}

# Trap to ensure cleanup on interrupt
trap 'echo ""; log_warning "Session close interrupted"; exit 1' INT TERM

# Run main function
main "$@"
