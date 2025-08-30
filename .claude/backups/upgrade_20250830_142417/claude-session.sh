#!/bin/bash
# Claude Session Manager - Automates knowledge capture

PROJECT_DIR="$(pwd)"
CLAUDE_DIR="$PROJECT_DIR/.claude"
SESSION_ID=$(date +%Y%m%d_%H%M%S)
MAX_TOKENS=160000

# Initialize if needed
[ ! -d "$CLAUDE_DIR" ] && mkdir -p "$CLAUDE_DIR/sessions"

echo "🚀 Starting Claude session $SESSION_ID"
echo "📊 Context limit: $MAX_TOKENS tokens"

# Capture initial state
git status --short > "$CLAUDE_DIR/sessions/${SESSION_ID}_start.txt" 2>/dev/null
git diff --stat >> "$CLAUDE_DIR/sessions/${SESSION_ID}_start.txt" 2>/dev/null

# Find recently modified files
find . -type f \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.md" \) -mmin -60 2>/dev/null | head -10 > "$CLAUDE_DIR/sessions/${SESSION_ID}_recent.txt"

# Create session marker
cat > "$CLAUDE_DIR/sessions/current.md" << MARKER
## Session: $SESSION_ID
Started: $(date)
Branch: $(git branch --show-current 2>/dev/null || echo "main")
Context Budget: $MAX_TOKENS tokens

### Recent Activity
$(tail -5 "$CLAUDE_DIR/sessions/${SESSION_ID}_recent.txt" 2>/dev/null || echo "No recent files")

### Current Tasks
- [ ] Add your current task here

### Session Goals
- [ ] Define session objectives
MARKER

# Update CLAUDE.md with session info
sed -i '' "s/Session Started:.*/Session Started: $(date +"%Y-%m-%d %H:%M:%S")/" CLAUDE.md 2>/dev/null || \
sed -i "s/Session Started:.*/Session Started: $(date +"%Y-%m-%d %H:%M:%S")/" CLAUDE.md 2>/dev/null

echo "✅ Session initialized"
echo "📝 Run './claude-commit.sh' after making changes"
echo "⚠️  Run './claude-emergency-reset.sh' if approaching limits"