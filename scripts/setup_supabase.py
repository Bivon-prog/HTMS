#!/usr/bin/env python
"""
Supabase Setup — redirects to the complete setup script.
Use: python scripts/setup_complete.py
"""
import subprocess
import sys
import os

if __name__ == '__main__':
    script = os.path.join(os.path.dirname(__file__), 'setup_complete.py')
    sys.exit(subprocess.call([sys.executable, script]))
