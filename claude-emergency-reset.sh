#!/bin/bash
# Emergency reset when approaching limits

echo "🚨 EMERGENCY RESET PROTOCOL INITIATED"

# 1. Save current state
BACKUP_NAME=".claude/sessions/archive/emergency-$(date +%s).tar.gz"
tar -czf "$BACKUP_NAME" CLAUDE.md knowledge.md .claude/cache.json 2>/dev/null

echo "✅ Current state backed up to: $BACKUP_NAME"

# 2. Create minimal context
cat > CLAUDE-MINIMAL.md << MINIMAL
## MINIMAL CONTEXT - EMERGENCY RESET
Project: picobrain
Time: $(date)
Last Good Commit: $(git log -1 --pretty=%H)

## Critical Information Only
$(head -20 CLAUDE.md)

## Continue From
- Check $BACKUP_NAME for full context
- Current task: [Specify what you were working on]
MINIMAL

# 3. Compress session logs
find .claude/sessions -name "*.txt" -mtime +1 -exec gzip {} \; 2>/dev/null

# 4. Clear large files
find .claude -type f -size +1M -exec rm {} \; 2>/dev/null

# 5. Reset cache
cat > .claude/cache.json << CACHE_RESET
{
  "lastUpdated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "projectName": "picobrain",
  "sessionSummary": "Emergency reset performed",
  "contextUsage": {"current": 1000, "max": 160000}
}
CACHE_RESET

echo "✅ Emergency reset complete"
echo "📝 Minimal context saved to CLAUDE-MINIMAL.md"
echo "🔄 Restart with: ./claude-session.sh --minimal"