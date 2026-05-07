#!/usr/bin/env python
"""Setup Appwrite Collections for HTMS"""
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
        
        # Create Users Collection
        print("👥 Creating Users Collection...")
        try:
            users_collection = databases.create_collection(
                database_id=database_id,
                collection_id='users',
                name='Users',
                permissions=[
                    "read",
                    "write",
                    "create",
                    "update",
                    "delete"
                ]
            )
            
            # Add user attributes
            attributes = [
                {'key': 'email', 'size': 255, 'required': True},
                {'key': 'first_name', 'size': 100, 'required': True},
                {'key': 'last_name', 'size': 100, 'required': True},
                {'key': 'password', 'size': 255, 'required': True},
                {'key': 'role', 'size': 50, 'required': True, 'default': 'Requester'},
                {'key': 'department', 'size': 50, 'required': False},
                {'key': 'mission', 'size': 50, 'required': False},
                {'key': 'timezone', 'size': 50, 'required': True, 'default': 'UTC'},
                {'key': 'is_active', 'required': True, 'default': True},
                {'key': 'is_staff', 'required': True, 'default': False},
                {'key': 'is_superuser', 'required': True, 'default': False},
                {'key': 'date_joined', 'required': True},
                {'key': 'last_login', 'required': False},
                {'key': 'created_at', 'required': True},
                {'key': 'updated_at', 'required': True},
            ]
            
            for attr in attributes:
                try:
                    databases.create_string_attribute(
                        database_id=database_id,
                        collection_id='users',
                        key=attr['key'],
                        size=attr.get('size', 255),
                        required=attr.get('required', False),
                        default=attr.get('default')
                    )
                    print(f"  ✅ Added attribute: {attr['key']}")
                except:
                    print(f"  ⚠️ Attribute already exists: {attr['key']}")
                    
        except AppwriteException as e:
            print(f"  ⚠️ Users collection might already exist: {e}")
        
        # Create Tickets Collection
        print("🎫 Creating Tickets Collection...")
        try:
            tickets_collection = databases.create_collection(
                database_id=database_id,
                collection_id='tickets',
                name='Tickets',
                permissions=[
                    "read",
                    "write",
                    "create",
                    "update",
                    "delete"
                ]
            )
            
            # Add ticket attributes
            ticket_attributes = [
                {'key': 'title', 'size': 255, 'required': True},
                {'key': 'description', 'size': 2000, 'required': True},
                {'key': 'status', 'size': 50, 'required': True, 'default': 'Open'},
                {'key': 'priority', 'size': 20, 'required': True, 'default': 'Medium'},
                {'key': 'category', 'size': 100, 'required': True},
                {'key': 'requester', 'size': 255, 'required': True},
                {'key': 'assigned_to', 'size': 255, 'required': False},
                {'key': 'mission', 'size': 50, 'required': True},
                {'key': 'created_at', 'required': True},
                {'key': 'updated_at', 'required': True},
                {'key': 'resolved_at', 'required': False},
                {'key': 'closed_at', 'required': False},
            ]
            
            for attr in ticket_attributes:
                try:
                    databases.create_string_attribute(
                        database_id=database_id,
                        collection_id='tickets',
                        key=attr['key'],
                        size=attr.get('size', 255),
                        required=attr.get('required', False),
                        default=attr.get('default')
                    )
                    print(f"  ✅ Added attribute: {attr['key']}")
                except:
                    print(f"  ⚠️ Attribute already exists: {attr['key']}")
                    
        except AppwriteException as e:
            print(f"  ⚠️ Tickets collection might already exist: {e}")
        
        # Create Missions Collection
        print("🌍 Creating Missions Collection...")
        try:
            missions_collection = databases.create_collection(
                database_id=database_id,
                collection_id='missions',
                name='Missions',
                permissions=[
                    "read",
                    "write",
                    "create",
                    "update",
                    "delete"
                ]
            )
            
            # Add mission attributes
            mission_attributes = [
                {'key': 'name', 'size': 255, 'required': True},
                {'key': 'code', 'size': 10, 'required': True},
                {'key': 'country', 'size': 100, 'required': True},
                {'key': 'city', 'size': 100, 'required': True},
                {'key': 'timezone', 'size': 50, 'required': True, 'default': 'UTC'},
                {'key': 'is_active', 'required': True, 'default': True},
                {'key': 'created_at', 'required': True},
                {'key': 'updated_at', 'required': True},
            ]
            
            for attr in mission_attributes:
                try:
                    databases.create_string_attribute(
                        database_id=database_id,
                        collection_id='missions',
                        key=attr['key'],
                        size=attr.get('size', 255),
                        required=attr.get('required', False),
                        default=attr.get('default')
                    )
                    print(f"  ✅ Added attribute: {attr['key']}")
                except:
                    print(f"  ⚠️ Attribute already exists: {attr['key']}")
                    
        except AppwriteException as e:
            print(f"  ⚠️ Missions collection might already exist: {e}")
        
        print("✅ Appwrite Collections Setup Complete!")
        
        # List all collections
        collections = databases.list_collections(database_id)
        print(f"📋 Total Collections: {len(collections.collections)}")
        for collection in collections.collections:
            print(f"  📁 {collection.name} ({collection['$id']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup Failed: {e}")
        return False

if __name__ == '__main__':
    setup_appwrite_collections()
