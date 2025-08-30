#!/usr/bin/env python3
"""Run administrative tasks for PicoBrain"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='PicoBrain Admin Tasks')
    parser.add_argument('task', choices=['create-admin'], help='Task to run')
    args = parser.parse_args()
    
    if args.task == 'create-admin':
        from app.seeds.create_admin import create_admin_user
        create_admin_user()
