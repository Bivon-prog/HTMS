#!/usr/bin/env python
"""Setup Appwrite Collections for HTMS with new API"""
import os
from pathlib import Path
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException

# Load environment variables
env_file = Path('.env')
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def setup_appwrite_collections():
    try:
        print("🚀 Setting up Appwrite Collections for HTMS...")
        
        # Initialize Appwrite client
        client = Client()
        client.set_endpoint(os.environ.get('APPWRITE_ENDPOINT'))
        client.set_project(os.environ.get('APPWRITE_PROJECT_ID'))
        client.set_key(os.environ.get('APPWRITE_API_KEY'))
        
        databases = Databases(client)
        database_id = os.environ.get('APPWRITE_DATABASE_ID')
        
        print(f"📊 Database ID: {database_id}")
        
        # Create Users Table
        print("👥 Creating Users Table...")
        try:
            users_table = databases.create_table(
                database_id=database_id,
                table_id='users',
                name='Users',
                permissions=[
                    "read(\"any\")",
                    "write(\"any\")",
                    "create(\"any\")",
                    "update(\"any\")",
                    "delete(\"any\")"
                ]
            )
            print("  ✅ Users table created")
        except AppwriteException as e:
            print(f"  ⚠️ Users table might already exist: {e}")
        
        # Create Tickets Table
        print("🎫 Creating Tickets Table...")
        try:
            tickets_table = databases.create_table(
                database_id=database_id,
                table_id='tickets',
                name='Tickets',
                permissions=[
                    "read(\"any\")",
                    "write(\"any\")",
                    "create(\"any\")",
                    "update(\"any\")",
                    "delete(\"any\")"
                ]
            )
            print("  ✅ Tickets table created")
        except AppwriteException as e:
            print(f"  ⚠️ Tickets table might already exist: {e}")
        
        # Create Missions Table
        print("🌍 Creating Missions Table...")
        try:
            missions_table = databases.create_table(
                database_id=database_id,
                table_id='missions',
                name='Missions',
                permissions=[
                    "read(\"any\")",
                    "write(\"any\")",
                    "create(\"any\")",
                    "update(\"any\")",
                    "delete(\"any\")"
                ]
            )
            print("  ✅ Missions table created")
        except AppwriteException as e:
            print(f"  ⚠️ Missions table might already exist: {e}")
        
        print("✅ Appwrite Tables Setup Complete!")
        
        # List all tables
        try:
            tables = databases.list_tables(database_id)
            print(f"📋 Total Tables: {len(tables.tables)}")
            for table in tables.tables:
                print(f"  📁 {table.name} ({table['$id']})")
        except Exception as e:
            print(f"  ⚠️ Could not list tables: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup Failed: {e}")
        return False

if __name__ == '__main__':
    setup_appwrite_collections()
