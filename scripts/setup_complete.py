#!/usr/bin/env python
"""
Complete HTMS Setup Script for Supabase Development
Runs migrations, creates superuser, loads missions and categories.

Usage: python scripts/setup_complete.py
"""
import os
import sys

# Add parent directory to path so we can import Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django

# Use Supabase settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'htms.settings_supabase')

def main():
    print("=" * 70)
    print("🚀 HTMS Complete Setup — Supabase Development")
    print("=" * 70)
    
    # Initialize Django
    django.setup()
    
    from django.core.management import call_command
    from django.db import connection
    from apps.authentication.models import User
    
    # ─── Step 1: Test Database Connection ────────────────────────────────────
    print("\n[1/6] Testing Supabase database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✓ Connected to PostgreSQL: {version[:50]}...")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease check your .env.supabase file:")
        print("  - SUPABASE_DB_HOST")
        print("  - SUPABASE_DB_NAME")
        print("  - SUPABASE_DB_USER")
        print("  - SUPABASE_DB_PASSWORD")
        sys.exit(1)
    
    # ─── Step 2: Run Migrations ───────────────────────────────────────────────
    print("\n[2/6] Creating database migrations...")
    try:
        call_command('makemigrations', verbosity=1)
        print("✓ Migrations created")
    except Exception as e:
        print(f"✗ Error creating migrations: {e}")
        sys.exit(1)
    
    print("\n[3/6] Applying migrations to database...")
    try:
        call_command('migrate', verbosity=1)
        print("✓ All migrations applied")
    except Exception as e:
        print(f"✗ Error applying migrations: {e}")
        sys.exit(1)
    
    # ─── Step 3: Load Missions & Categories ───────────────────────────────────
    print("\n[4/6] Loading 70 missions and ticket categories...")
    try:
        call_command('load_missions', verbosity=1)
        print("✓ Missions and categories loaded")
    except Exception as e:
        print(f"✗ Error loading missions: {e}")
        sys.exit(1)
    
    # ─── Step 4: Create Superuser ─────────────────────────────────────────────
    print("\n[5/6] Creating HQ Super Admin user...")
    
    admin_email = input("  Enter admin email [admin@htms.go.ke]: ").strip() or "admin@htms.go.ke"
    admin_first = input("  Enter first name [Admin]: ").strip() or "Admin"
    admin_last = input("  Enter last name [User]: ").strip() or "User"
    admin_password = input("  Enter password [admin123]: ").strip() or "admin123"
    
    if User.objects.filter(email=admin_email).exists():
        print(f"  ⚠ User {admin_email} already exists, skipping...")
    else:
        try:
            user = User.objects.create_superuser(
                email=admin_email,
                first_name=admin_first,
                last_name=admin_last,
                password=admin_password,
            )
            user.role = 'HQ_Super_Admin'
            user.save(update_fields=['role'])
            print(f"  ✓ Superuser created: {admin_email}")
            print(f"    Password: {admin_password}")
        except Exception as e:
            print(f"  ✗ Error creating superuser: {e}")
            sys.exit(1)
    
    # ─── Step 5: Collect Static Files ─────────────────────────────────────────
    print("\n[6/6] Collecting static files...")
    try:
        call_command('collectstatic', '--noinput', verbosity=0)
        print("✓ Static files collected")
    except Exception as e:
        print(f"  ⚠ Static files warning: {e}")
    
    # ─── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("✅ HTMS Setup Complete!")
    print("=" * 70)
    
    from apps.missions.models import Mission, TicketCategory
    mission_count = Mission.objects.count()
    category_count = TicketCategory.objects.count()
    user_count = User.objects.count()
    
    print(f"\n📊 Database Summary:")
    print(f"   • {mission_count} missions loaded")
    print(f"   • {category_count} ticket categories")
    print(f"   • {user_count} user(s) created")
    
    print(f"\n🔐 Login Credentials:")
    print(f"   Email:    {admin_email}")
    print(f"   Password: {admin_password}")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Start backend:  python manage_supabase.py runserver")
    print(f"   2. Start frontend: cd frontend && npm start")
    print(f"   3. Open browser:   http://localhost:3000")
    print(f"   4. Admin panel:    http://localhost:8000/admin/")
    print(f"\n📖 Documentation:  docs/START_HERE.md")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
