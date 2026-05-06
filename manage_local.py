#!/usr/bin/env python
"""Django management utility using local SQLite database.
Use this when Supabase is unavailable.

Usage: python manage_local.py runserver
"""
import os
import sys


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'htms.settings_local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Activate your virtual environment: "
            "venv\\Scripts\\activate"
        ) from exc
    execute_from_command_line(sys.argv)
