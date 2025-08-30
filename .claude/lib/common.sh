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
