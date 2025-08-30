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
