#!/bin/bash
# Claude Knowledge Base v2.0 - Complete Automated Upgrade
# This script upgrades existing KB to v2.0 with enhanced features

set -euo pipefail

# ============================================
# CONFIGURATION
# ============================================
PROJECT_PATH="/Users/edo/PyProjects/picobrain"
PROJECT_NAME="PicoBrain"
CLAUDE_DIR="$PROJECT_PATH/.claude"
BACKUP_DIR="$CLAUDE_DIR/backups/upgrade_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="$CLAUDE_DIR/logs/upgrade_$(date +%Y%m%d_%H%M%S).log"
PYTHON_CMD="python3"
MAX_CONTEXT_TOKENS="160000"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ============================================
# HELPER FUNCTIONS
# ============================================
log() {
    echo -e "${2:-}[$(date +'%H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

error_exit() {
    log "ERROR: $1" "$RED"
    exit 1
}

success() {
    log "✅ $1" "$GREEN"
}

warning() {
    log "⚠️  $1" "$YELLOW"
}

create_directory() {
    if mkdir -p "$1" 2>/dev/null; then
        success "Created: $1"
    else
        error_exit "Failed to create directory: $1"
    fi
}

# ============================================
# PHASE 1: BACKUP EXISTING SETUP
# ============================================
phase1_backup() {
    log "===== PHASE 1: Backing Up Existing Setup =====" "$YELLOW"
    
    create_directory "$BACKUP_DIR"
    
    # Backup existing files
    for item in CLAUDE.md knowledge.md .claude claude-*.sh; do
        if [ -e "$PROJECT_PATH/$item" ]; then
            cp -r "$PROJECT_PATH/$item" "$BACKUP_DIR/" 2>/dev/null || warning "Could not backup $item"
        fi
    done
    
    success "Backup complete: $BACKUP_DIR"
}

# ============================================
# PHASE 2: ENHANCE DIRECTORY STRUCTURE
# ============================================
phase2_enhance_structure() {
    log "===== PHASE 2: Enhancing Directory Structure =====" "$YELLOW"
    
    local dirs=(
        "$CLAUDE_DIR/lib"
        "$CLAUDE_DIR/hooks"
        "$CLAUDE_DIR/knowledge"
        "$CLAUDE_DIR/validation"
        "$CLAUDE_DIR/logs"
        "$CLAUDE_DIR/backups"
    )
    
    for dir in "${dirs[@]}"; do
        create_directory "$dir"
    done
    
    success "Enhanced directory structure created"
}

# ============================================
# PHASE 3: INSTALL COMMON LIBRARY
# ============================================
phase3_install_library() {
    log "===== PHASE 3: Installing Common Library =====" "$YELLOW"
    
    cat > "$CLAUDE_DIR/lib/common.sh" << 'EOFLIB'
#!/bin/bash
# Common functions for Claude KB scripts

# Logging with levels
log() {
    local level=$1
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*" >> "${LOG_FILE:-/dev/stdout}"
}

# Atomic file write
atomic_write() {
    local target_file=$1
    local content=$2
    local tmp_file=$(mktemp)
    
    echo "$content" > "$tmp_file"
    mv -f "$tmp_file" "$target_file"
}

# File locking
acquire_lock() {
    local lock_file=$1
    local timeout=${2:-10}
    local elapsed=0
    
    while [ $elapsed -lt $timeout ]; do
        if mkdir "$lock_file" 2>/dev/null; then
            return 0
        fi
        sleep 1
        elapsed=$((elapsed + 1))
    done
    
    return 1
}

release_lock() {
    rm -rf "$1"
}

# Token estimation
estimate_tokens() {
    local file=$1
    if [ -f "$file" ]; then
        local chars=$(wc -c < "$file")
        echo $((chars / 4))
    else
        echo 0
    fi
}

# Git helpers
get_current_branch() {
    git branch --show-current 2>/dev/null || echo "main"
}

get_last_commit() {
    git log -1 --pretty=format:"%h - %s" 2>/dev/null || echo "No commits yet"
}
EOFLIB
    
    chmod +x "$CLAUDE_DIR/lib/common.sh"
    success "Common library installed"
}

# ============================================
# PHASE 4: ENHANCE KNOWLEDGE FILES
# ============================================
phase4_enhance_knowledge_files() {
    log "===== PHASE 4: Enhancing Knowledge Files =====" "$YELLOW"
    
    # Update CLAUDE.md with Claude-specific markers
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local session_id=$(date +%Y%m%d_%H%M%S)
    local branch=$(git branch --show-current 2>/dev/null || echo "main")
    local last_commit=$(git log -1 --pretty=format:"%h - %s" 2>/dev/null || echo "No commits")
    
    # Backup existing CLAUDE.md content
    local existing_content=""
    if [ -f "$PROJECT_PATH/CLAUDE.md" ]; then
        existing_content=$(tail -n +20 "$PROJECT_PATH/CLAUDE.md" 2>/dev/null || echo "")
    fi
    
    cat > "$PROJECT_PATH/CLAUDE.md" << EOF
<!-- CLAUDE: ALWAYS READ THIS FIRST - ACTIVE PROJECT CONTEXT -->
<!-- Last Updated: $timestamp -->
<!-- Session ID: $session_id -->

# 🧠 CLAUDE KNOWLEDGE BASE - $PROJECT_NAME

## 🚨 PRIORITY CONTEXT (Read First)
**Project**: $PROJECT_NAME
**Location**: $PROJECT_PATH
**Session**: Active since $timestamp
**Context Usage**: 0 / $MAX_CONTEXT_TOKENS tokens

## 📊 CURRENT STATE
\`\`\`yaml
branch: $branch
last_commit: $last_commit
active_files: []
pending_tasks: []
\`\`\`

## 🎯 SESSION OBJECTIVES
- [ ] Implement Claude KB v2.0 improvements
- [ ] Enhance automation and pattern extraction
- [ ] Validate setup completeness

## 📄 RECENT ACTIVITY
$existing_content
EOF
    
    success "Knowledge files enhanced with Claude markers"
}

# ============================================
# PHASE 5: INSTALL PYTHON COMPONENTS
# ============================================
phase5_install_python() {
    log "===== PHASE 5: Installing Python Components =====" "$YELLOW"
    
    # Check and install Python packages
    log "Checking Python dependencies..."
    
    # Create requirements file
    cat > "$CLAUDE_DIR/requirements.txt" << 'EOF'
watchdog>=3.0.0
tiktoken>=0.5.0
EOF
    
    # Install packages
    "$PYTHON_CMD" -m pip install -q -r "$CLAUDE_DIR/requirements.txt" 2>/dev/null || warning "Some Python packages may need manual installation"
    
    # Create pattern extractor
    cat > "$CLAUDE_DIR/lib/pattern_extractor.py" << 'EOFPY'
#!/usr/bin/env python3
"""Advanced pattern extraction with AST parsing"""

import ast
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class PatternExtractor:
    def __init__(self):
        self.claude_dir = Path(".claude")
        self.patterns_db = self.claude_dir / "knowledge" / "patterns.json"
        self.ensure_db()
    
    def ensure_db(self):
        if not self.patterns_db.exists():
            self.patterns_db.parent.mkdir(parents=True, exist_ok=True)
            self.patterns_db.write_text(json.dumps({
                "patterns": [],
                "antipatterns": [],
                "last_updated": datetime.now().isoformat()
            }, indent=2))
    
    def extract_from_file(self, filepath: Path):
        """Extract patterns based on file type"""
        if filepath.suffix == '.py':
            return self.extract_python_patterns(filepath)
        elif filepath.suffix in ['.js', '.jsx', '.ts', '.tsx']:
            return self.extract_javascript_patterns(filepath)
        return []
    
    def extract_python_patterns(self, filepath: Path):
        """Extract patterns from Python using AST"""
        patterns = []
        try:
            content = filepath.read_text()
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.decorator_list:
                        patterns.append({
                            "type": "decorator",
                            "file": str(filepath),
                            "pattern": f"@decorators on {node.name}",
                            "confidence": 0.9
                        })
                
                elif isinstance(node, ast.ClassDef):
                    if node.bases:
                        patterns.append({
                            "type": "inheritance",
                            "file": str(filepath),
                            "pattern": f"class {node.name}",
                            "confidence": 0.95
                        })
        except:
            pass
        
        return patterns
    
    def extract_javascript_patterns(self, filepath: Path):
        """Extract patterns from JavaScript/TypeScript"""
        patterns = []
        try:
            content = filepath.read_text()
            
            # React hooks
            if 'useState' in content or 'useEffect' in content:
                patterns.append({
                    "type": "react_hooks",
                    "file": str(filepath),
                    "pattern": "React functional component with hooks",
                    "confidence": 0.85
                })
            
            # Async patterns
            if 'async' in content and 'await' in content:
                patterns.append({
                    "type": "async_await",
                    "file": str(filepath),
                    "pattern": "Async/await pattern",
                    "confidence": 0.8
                })
        except:
            pass
        
        return patterns
    
    def save_patterns(self, patterns: List[Dict]):
        """Save patterns to database"""
        db = json.loads(self.patterns_db.read_text())
        db["patterns"].extend(patterns)
        db["last_updated"] = datetime.now().isoformat()
        db["patterns"] = db["patterns"][-500:]  # Keep last 500
        self.patterns_db.write_text(json.dumps(db, indent=2))
        return len(patterns)

def main():
    import subprocess
    
    extractor = PatternExtractor()
    result = subprocess.run(['git', 'diff', '--name-only'], 
                          capture_output=True, text=True)
    
    all_patterns = []
    for filepath in result.stdout.strip().split('\n'):
        if filepath:
            path = Path(filepath)
            if path.exists():
                patterns = extractor.extract_from_file(path)
                all_patterns.extend(patterns)
    
    if all_patterns:
        count = extractor.save_patterns(all_patterns)
        print(f"✅ Extracted {count} patterns")
    else:
        print("No patterns found in changes")

if __name__ == "__main__":
    main()
EOFPY
    
    chmod +x "$CLAUDE_DIR/lib/pattern_extractor.py"
    success "Python components installed"
}

# ============================================
# PHASE 6: UPGRADE SCRIPTS
# ============================================
phase6_upgrade_scripts() {
    log "===== PHASE 6: Upgrading Shell Scripts =====" "$YELLOW"
    
    # Enhanced claude-session.sh
    cat > "$PROJECT_PATH/claude-session.sh" << 'EOFSESSION'
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
EOFSESSION
    
    chmod +x "$PROJECT_PATH/claude-session.sh"
    
    # Create validation script
    cat > "$PROJECT_PATH/claude-validate.sh" << 'EOFVAL'
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
EOFVAL
    
    chmod +x "$PROJECT_PATH/claude-validate.sh"
    
    success "Scripts upgraded"
}

# ============================================
# PHASE 7: SETUP GIT HOOKS
# ============================================
phase7_git_hooks() {
    log "===== PHASE 7: Setting Up Git Hooks =====" "$YELLOW"
    
    # Enhanced post-commit hook
    cat > "$PROJECT_PATH/.git/hooks/post-commit" << 'EOFHOOK'
#!/bin/bash
# Auto-update knowledge base after commits

(
    cd "$(git rev-parse --show-toplevel)"
    
    # Extract patterns if Python extractor exists
    if [ -x ".claude/lib/pattern_extractor.py" ]; then
        python3 .claude/lib/pattern_extractor.py 2>/dev/null || true
    fi
    
    # Update metrics
    commit_hash=$(git rev-parse HEAD)
    commit_msg=$(git log -1 --pretty=%B)
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Log based on commit type
    if [[ "$commit_msg" == feat:* ]]; then
        echo "$timestamp|FEATURE|$commit_hash|$commit_msg" >> .claude/patterns/features.log
    elif [[ "$commit_msg" == fix:* ]]; then
        echo "$timestamp|FIX|$commit_hash|$commit_msg" >> .claude/errors/fixes.log
    fi
    
    # Update CLAUDE.md with latest commit
    if [ -f "CLAUDE.md" ]; then
        sed -i.bak "s|last_commit: .*|last_commit: $commit_hash - ${commit_msg:0:50}|" CLAUDE.md
        rm -f CLAUDE.md.bak
    fi
) &
EOFHOOK
    
    chmod +x "$PROJECT_PATH/.git/hooks/post-commit"
    
    success "Git hooks installed"
}

# ============================================
# PHASE 8: FINAL VALIDATION
# ============================================
phase8_validate() {
    log "===== PHASE 8: Final Validation =====" "$YELLOW"
    
    # Run validation script
    if [ -x "$PROJECT_PATH/claude-validate.sh" ]; then
        "$PROJECT_PATH/claude-validate.sh"
    fi
    
    success "Validation complete"
}

# ============================================
# MAIN EXECUTION
# ============================================
main() {
    echo "======================================"
    echo "Claude Knowledge Base v2.0 Upgrade"
    echo "======================================"
    echo "Project: $PROJECT_NAME"
    echo "Path: $PROJECT_PATH"
    echo "======================================"
    
    # Create log directory first
    mkdir -p "$CLAUDE_DIR/logs"
    
    # Execute all phases
    phase1_backup
    phase2_enhance_structure
    phase3_install_library
    phase4_enhance_knowledge_files
    phase5_install_python
    phase6_upgrade_scripts
    phase7_git_hooks
    phase8_validate
    
    echo ""
    echo "======================================"
    echo "✅ UPGRADE COMPLETE!"
    echo "======================================"
    echo ""
    echo "🚀 Quick Start:"
    echo "  1. Run: ./claude-session.sh"
    echo "  2. Run: ./claude-validate.sh"
    echo ""
    echo "📚 Knowledge files ready:"
    echo "  - CLAUDE.md (with Claude markers)"
    echo "  - knowledge.md (accumulated knowledge)"
    echo ""
    echo "🔄 Automation enabled:"
    echo "  - Git hooks capture patterns"
    echo "  - Knowledge updates automatically"
    echo "  - Python pattern extraction ready"
    echo ""
    echo "💡 Claude will now automatically read your knowledge base!"
    echo "======================================"
}

# Run main
main "$@"
