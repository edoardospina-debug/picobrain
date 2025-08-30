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
