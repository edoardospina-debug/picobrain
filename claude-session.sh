#!/bin/bash
set -euo pipefail

# Source common library
source .claude/lib/common.sh 2>/dev/null || true

PROJECT_DIR="$(pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
SESSION_ID=$(date +%Y%m%d_%H%M%S)
MAX_CONTEXT_TOKENS=160000

# Ensure Claude reads our knowledge
ensure_knowledge_visibility() {
    for file in CLAUDE.md knowledge.md; do
        if [ ! -f "$file" ]; then
            echo "ERROR: Missing $file - Creating default..."
            touch "$file"
        fi
    done
    
    # Update timestamp to ensure fresh read
    touch CLAUDE.md knowledge.md
    
    # Calculate token usage
    local tokens=$(estimate_tokens CLAUDE.md 2>/dev/null || echo "0")
    tokens=$((tokens + $(estimate_tokens knowledge.md 2>/dev/null || echo "0")))
    
    # Update token count in CLAUDE.md
    sed -i.bak "s|Context Usage: .* tokens|Context Usage: $tokens / $MAX_CONTEXT_TOKENS tokens|" CLAUDE.md
    rm -f CLAUDE.md.bak
}

main() {
    echo "🚀 Starting session $SESSION_ID"
    
    ensure_knowledge_visibility
    
    # Update CLAUDE.md with session info
    sed -i.bak "s|<!-- Session ID: .* -->|<!-- Session ID: $SESSION_ID -->|" CLAUDE.md
    sed -i.bak "s|<!-- Last Updated: .* -->|<!-- Last Updated: $(date +'%Y-%m-%d %H:%M:%S') -->|" CLAUDE.md
    rm -f CLAUDE.md.bak
    
    # Capture current state
    {
        echo "Session: $SESSION_ID"
        echo "Started: $(date)"
        echo "Branch: $(git branch --show-current 2>/dev/null || echo 'main')"
        echo "Recent files:"
        find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \) -mmin -60 2>/dev/null | head -10
    } > "$CLAUDE_DIR/sessions/current.md"
    
    echo "✅ Session initialized. Claude will read CLAUDE.md and knowledge.md automatically."
}

# Define estimate_tokens if not sourced from common.sh
if ! declare -f estimate_tokens > /dev/null; then
    estimate_tokens() {
        if [ -f "$1" ]; then
            echo $(($(wc -c < "$1") / 4))
        else
            echo 0
        fi
    }
fi

main "$@"
