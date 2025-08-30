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
