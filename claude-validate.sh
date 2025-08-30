#!/bin/bash
# Validate knowledge base setup

ERRORS=0
WARNINGS=0

check() {
    if eval "$1"; then
        echo "✅ $2"
    else
        echo "❌ $2"
        ((ERRORS++))
    fi
}

warn_check() {
    if eval "$1"; then
        echo "✅ $2"
    else
        echo "⚠️  $2"
        ((WARNINGS++))
    fi
}

echo "🔍 Validating Claude Knowledge Base Setup..."
echo "==========================================="

check "[ -f CLAUDE.md ]" "CLAUDE.md exists"
check "[ -f knowledge.md ]" "knowledge.md exists"
check "[ -d .claude ]" ".claude directory exists"
check "[ -x claude-session.sh ]" "claude-session.sh is executable"
check "command -v git >/dev/null" "Git is installed"
warn_check "command -v python3 >/dev/null" "Python 3 is installed"

# Check knowledge file headers
check "grep -q 'CLAUDE: ALWAYS READ THIS FIRST' CLAUDE.md" "CLAUDE.md has correct header"

# Check git hooks
warn_check "[ -f .git/hooks/post-commit ]" "Git post-commit hook installed"

echo "==========================================="
echo "Results: $ERRORS errors, $WARNINGS warnings"

if [ $ERRORS -eq 0 ]; then
    echo "✅ Knowledge base is properly configured!"
    exit 0
else
    echo "❌ Please fix errors before proceeding"
    exit 1
fi
