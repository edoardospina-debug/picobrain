#!/bin/bash
# Extracts learnings from git diff and updates knowledge

CHANGES=$(git diff --stat 2>/dev/null || echo "No changes")
ADDITIONS=$(git diff --numstat 2>/dev/null | awk '{sum+=$1} END {print sum}' || echo "0")
DELETIONS=$(git diff --numstat 2>/dev/null | awk '{sum+=$2} END {print sum}' || echo "0")
MODIFIED_FILES=$(git diff --name-only 2>/dev/null | wc -l | tr -d ' ')
SESSION_TIME=$(date +"%Y-%m-%d %H:%M")

# Update CLAUDE.md with changes
cat >> CLAUDE.md << CHANGES_LOG

## Session Update: $SESSION_TIME
- **Changes**: $ADDITIONS additions, $DELETIONS deletions
- **Files modified**: $MODIFIED_FILES
- **Summary**: $CHANGES

### Patterns Observed
$(git diff 2>/dev/null | grep -E "^[+].*function|^[+].*const.*=|^[+].*class" | head -5 || echo "- No patterns extracted")

---
CHANGES_LOG

# Extract successful patterns
if [ "$ADDITIONS" -gt "50" ]; then
    echo "$(date): Large addition ($ADDITIONS lines) - potential new feature" >> .claude/patterns/features.log
fi

# Log the commit for pattern extraction
echo "$(date)|$ADDITIONS|$DELETIONS|$MODIFIED_FILES" >> .claude/metrics/changes.csv

# Update cache
jq --arg summary "Modified $MODIFIED_FILES files, +$ADDITIONS -$DELETIONS lines" \
   '.sessionSummary = $summary | .lastUpdated = now | .contextUsage.current = '$ADDITIONS'' \
   .claude/cache.json > .claude/cache.tmp && mv .claude/cache.tmp .claude/cache.json 2>/dev/null

echo "✅ Changes captured and knowledge updated"
echo "📊 Stats: +$ADDITIONS -$DELETIONS lines across $MODIFIED_FILES files"