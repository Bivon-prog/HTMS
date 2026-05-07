"""
Appwrite Service for HTMS
Handles all Appwrite database operations
"""

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.users import Users
from appwrite.exception import AppwriteException
from decouple import config
import json
from datetime import datetime

class AppwriteService:
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint(config('APPWRITE_ENDPOINT'))
        self.client.set_project(config('APPWRITE_PROJECT_ID'))
        self.client.set_key(config('APPWRITE_API_KEY'))
        
        self.databases = Databases(self.client)
        self.users = Users(self.client)
        self.database_id = config('APPWRITE_DATABASE_ID')
        
    def test_connection(self):
        """Test Appwrite connection"""
        try:
            # Try to list databases to test connection
            databases = self.client.databases.list()
            return True, "Connection successful"
        except AppwriteException as e:
            return False, str(e)
        except Exception as e:
            return False, str(e)
    
    def create_collection(self, collection_name, attributes):
        """Create a collection in Appwrite"""
        try:
            collection = self.databases.create_collection(
                database_id=self.database_id,
                collection_id=collection_name.lower(),
                name=collection_name,
                permissions=[
                    "read",
                    "write",
                    "create",
                    "update",
                    "delete"
                ]
            )
            
            # Add attributes
            for attr in attributes:
                self.databases.create_attribute(
                    database_id=self.database_id,
                    collection_id=collection_name.lower(),
                    key=attr['key'],
                    size=attr.get('size', 255),
                    required=attr.get('required', False),
                    default=attr.get('default'),
                    array=attr.get('array', False)
                )
            
            return True, collection
        except AppwriteException as e:
            return False, str(e)
    
    def create_document(self, collection_name, document_data, document_id=None):
        """Create a document in Appwrite"""
        try:
            if document_id:
                document = self.databases.create_document(
                    database_id=self.database_id,
                    collection_id=collection_name.lower(),
                    document_id=document_id,
                    data=document_data
                )
            else:
                document = self.databases.create_document(
                    database_id=self.database_id,
                    collection_id=collection_name.lower(),
                    data=document_data
                )
            return True, document
        except AppwriteException as e:
            return False, str(e)
    
    def get_document(self, collection_name, document_id):
        """Get a document from Appwrite"""
        try:
            document = self.databases.get_document(
                database_id=self.database_id,
                collection_id=collection_name.lower(),
                document_id=document_id
            )
            return True, document
        except AppwriteException as e:
            return False, str(e)
    
    def list_documents(self, collection_name, queries=None):
        """List documents from Appwrite"""
        try:
            documents = self.databases.list_documents(
                database_id=self.database_id,
                collection_id=collection_name.lower(),
                queries=queries or []
            )
            return True, documents
        except AppwriteException as e:
            return False, str(e)
    
    def update_document(self, collection_name, document_id, document_data):
        """Update a document in Appwrite"""
        try:
            document = self.databases.update_document(
                database_id=self.database_id,
                collection_id=collection_name.lower(),
                document_id=document_id,
                data=document_data
            )
            return True, document
        except AppwriteException as e:
            return False, str(e)
    
    def delete_document(self, collection_name, document_id):
        """Delete a document from Appwrite"""
        try:
            document = self.databases.delete_document(
                database_id=self.database_id,
                collection_id=collection_name.lower(),
                document_id=document_id
            )
            return True, document
        except AppwriteException as e:
            return False, str(e)

# Global instance
appwrite_service = AppwriteService()
