#!/bin/bash
# Complete Picobrain Setup Script - Run this to finish the setup
# Usage: bash complete-setup.sh

echo "🚀 Completing Picobrain automation setup..."
cd /Users/edo/PyProjects/picobrain

# ============================================
# 2.4 Context Monitor Script
# ============================================
cat > claude-context-monitor.sh << 'EOF'
#!/bin/bash
# Monitors context usage and provides warnings

# Calculate approximate token usage
CLAUDE_TOKENS=$(wc -w CLAUDE.md 2>/dev/null | awk '{print int($1 * 1.3)}' || echo "0")
KNOWLEDGE_TOKENS=$(wc -w knowledge.md 2>/dev/null | awk '{print int($1 * 1.3)}' || echo "0")
CACHE_SIZE=$(du -k .claude/cache.json 2>/dev/null | cut -f1 || echo "0")
TOTAL_TOKENS=$((CLAUDE_TOKENS + KNOWLEDGE_TOKENS))
MAX_TOKENS=160000
PERCENTAGE=$((TOTAL_TOKENS * 100 / MAX_TOKENS))

echo "📊 CONTEXT USAGE REPORT"
echo "========================"
echo "CLAUDE.md:     ~$CLAUDE_TOKENS tokens"
echo "knowledge.md:  ~$KNOWLEDGE_TOKENS tokens"
echo "Cache size:    ${CACHE_SIZE}KB"
echo "------------------------"
echo "Total:         ~$TOTAL_TOKENS / $MAX_TOKENS tokens ($PERCENTAGE%)"
echo ""

if [ $PERCENTAGE -gt 80 ]; then
    echo "⚠️  WARNING: Approaching token limit!"
    echo "🔧 Run './claude-emergency-reset.sh' to reset"
elif [ $PERCENTAGE -gt 60 ]; then
    echo "⚠️  CAUTION: Context usage high"
    echo "💡 Consider archiving old sessions"
else
    echo "✅ Context usage healthy"
fi

# Update cache with current usage
jq --arg current "$TOTAL_TOKENS" --arg max "$MAX_TOKENS" \
   '.contextUsage.current = ($current | tonumber) | .contextUsage.max = ($max | tonumber)' \
   .claude/cache.json > .claude/cache.tmp && mv .claude/cache.tmp .claude/cache.json 2>/dev/null
EOF

chmod +x claude-context-monitor.sh
echo "✅ Created claude-context-monitor.sh"

# ============================================
# Phase 3: Git Hooks Setup
# ============================================
echo "📝 Setting up Git hooks..."

# Create post-commit hook
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Auto-extract patterns from commits (runs in background)

(
  COMMIT_HASH=$(git rev-parse HEAD)
  COMMIT_MSG=$(git log -1 --pretty=%B)
  COMMIT_TIME=$(date +"%Y-%m-%d %H:%M:%S")
  
  # Log commit type for pattern extraction
  if [[ "$COMMIT_MSG" == feat:* ]]; then
    echo "$COMMIT_TIME|FEATURE|$COMMIT_HASH|$COMMIT_MSG" >> .claude/patterns/successes.log
    git diff HEAD~1 --name-only | head -5 >> .claude/patterns/feature_files.log
  elif [[ "$COMMIT_MSG" == fix:* ]]; then
    echo "$COMMIT_TIME|FIX|$COMMIT_HASH|$COMMIT_MSG" >> .claude/errors/fixes.log
    git diff HEAD~1 | grep -E "^[-]" | head -10 >> .claude/errors/removed_code.log
  elif [[ "$COMMIT_MSG" == refactor:* ]]; then
    echo "$COMMIT_TIME|REFACTOR|$COMMIT_HASH|$COMMIT_MSG" >> .claude/patterns/refactors.log
  fi
  
  # Compress logs if they exceed 1MB
  find .claude -name "*.log" -size +1M -exec gzip {} \;
) &
EOF

chmod +x .git/hooks/post-commit
echo "✅ Created post-commit hook"

# Create pre-push hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
# Remind to update knowledge before pushing

echo "📝 Reminder: Update knowledge base before pushing?"
echo "   Run: ./claude-commit.sh"
echo ""
EOF

chmod +x .git/hooks/pre-push
echo "✅ Created pre-push hook"

# ============================================
# Phase 4: Custom Commands
# ============================================
echo "🎨 Creating custom commands..."

# Create search-pattern command
cat > .claude/commands/search-pattern.md << 'EOF'
---
name: search-pattern
description: Search for a specific pattern in the knowledge base
---

Search for the pattern "$ARGUMENTS" in:
1. Check .claude/patterns/ directory for successful implementations
2. Check .claude/errors/ for related failures
3. Search knowledge.md for documentation
4. Return the most relevant 3 examples with context
EOF
echo "✅ Created search-pattern command"

# Create session-summary command
cat > .claude/commands/session-summary.md << 'EOF'
---
name: session-summary
description: Generate a summary of the current session
---

Generate a session summary including:
1. Files modified (from git status)
2. Patterns used successfully
3. Errors encountered and resolved
4. Time spent (from session start time)
5. Recommendations for next session
Update knowledge.md with any new learnings.
EOF
echo "✅ Created session-summary command"

# ============================================
# Phase 5: Weekly Automation
# ============================================
echo "📅 Setting up weekly review script..."

cat > claude-weekly-review.sh << 'EOF'
#!/bin/bash
# Weekly knowledge base maintenance and review

echo "📊 WEEKLY REVIEW - $(date +"%Y-W%V")"
echo "======================================"

# Archive old sessions
find .claude/sessions -name "*.txt" -mtime +7 -exec gzip {} \; 2>/dev/null
find .claude/sessions/archive -name "*.gz" -mtime +30 -delete 2>/dev/null

# Generate metrics
TOTAL_COMMITS=$(git log --since="1 week ago" --oneline 2>/dev/null | wc -l | tr -d ' ')
TOTAL_FILES_CHANGED=$(git log --since="1 week ago" --name-only --pretty=format: 2>/dev/null | sort -u | wc -l | tr -d ' ')

# Update knowledge.md with weekly summary
cat >> knowledge.md << WEEKLY
## Weekly Review: $(date +"%Y-W%V")
- Commits: $TOTAL_COMMITS
- Files Changed: $TOTAL_FILES_CHANGED
- Top patterns: $(head -3 .claude/patterns/successes.log 2>/dev/null || echo "None yet")
---
WEEKLY

# Prune unused patterns (over 30 days old)
find .claude/patterns -name "*.log" -mtime +30 -size 0 -delete 2>/dev/null

echo "✅ Weekly review complete"
echo "📈 Progress: $TOTAL_COMMITS commits, $TOTAL_FILES_CHANGED files modified"
EOF

chmod +x claude-weekly-review.sh
echo "✅ Created claude-weekly-review.sh"

# ============================================
# Phase 6: MCP Server Configuration
# ============================================
echo "🔧 Checking MCP configuration..."

CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ -f "$CLAUDE_CONFIG" ]; then
  echo "📝 Claude Desktop config found. Add this to your config:"
  echo '{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/edo/PyProjects/picobrain"
      ]
    },
    "fast-filesystem": {
      "command": "npx",
      "args": ["-y", "fast-filesystem-mcp"],
      "env": {
        "CREATE_BACKUP_FILES": "false",
        "BATCH_MODE": "true",
        "CACHE_ENABLED": "true"
      }
    }
  }
}'
else
  echo "⚠️  Claude Desktop config not found. MCP setup skipped."
fi

# ============================================
# Phase 7: Testing & Validation
# ============================================
echo ""
echo "🔍 Validating setup..."
echo "====================="

SCRIPTS=(
  "claude-session.sh"
  "claude-commit.sh"
  "claude-emergency-reset.sh"
  "claude-context-monitor.sh"
  "claude-weekly-review.sh"
)

for script in "${SCRIPTS[@]}"; do
  if [ -x "$script" ]; then
    echo "✅ $script is ready"
  else
    echo "❌ $script missing or not executable"
  fi
done

# Check knowledge files
[ -f "CLAUDE.md" ] && echo "✅ CLAUDE.md exists" || echo "❌ CLAUDE.md missing"
[ -f "knowledge.md" ] && echo "✅ knowledge.md exists" || echo "❌ knowledge.md missing"
[ -d ".claude" ] && echo "✅ .claude directory exists" || echo "❌ .claude directory missing"

echo ""
echo "📊 Running initial context monitor..."
echo "====================================="
./claude-context-monitor.sh

echo ""
echo "✨ SETUP COMPLETE!"
echo "=================="
echo ""
echo "📚 Quick Start Guide:"
echo "--------------------"
echo "1. Start a session:     ./claude-session.sh"
echo "2. After changes:       ./claude-commit.sh"
echo "3. Check usage:         ./claude-context-monitor.sh"
echo "4. If limits reached:   ./claude-emergency-reset.sh"
echo "5. Weekly maintenance:  ./claude-weekly-review.sh"
echo ""
echo "💡 Pro Tips:"
echo "-----------"
echo "• Monitor memory with Activity Monitor during heavy operations"
echo "• Use context monitor before long sessions"
echo "• Archive old sessions monthly"
echo "• Update knowledge.md after significant learnings"
echo ""
echo "🎉 Happy coding with automated knowledge capture!"