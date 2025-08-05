#!/usr/bin/env python3
"""
Notion for DS - A program to store messages in Notion databases
"""

import os
import sys
import json
from dotenv import load_dotenv
from notion_client import Client

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    # Load individual environment variables
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    # Load configurable database properties
    message_property = os.getenv('NOTION_MESSAGE_PROPERTY', 'Message')
    name_property = os.getenv('NOTION_NAME_PROPERTY', 'Name')
    
    if not notion_token:
        print("Error: NOTION_TOKEN not found in environment variables")
        print("Please create a .env file with your Notion integration token")
        sys.exit(1)
        
    if not database_id:
        print("Error: NOTION_DATABASE_ID not found in environment variables")
        print("Please create a .env file with your Notion database ID")
        sys.exit(1)
        
    return notion_token, database_id, message_property, name_property

def store_in_notion_database(client, database_id, message, message_property='Message', name_property='Name'):
    """Store a message in the specified Notion database"""
    try:
        # Create a new page in the database
        response = client.pages.create(
            parent={"database_id": database_id},
            properties={
                message_property: {
                    "title": [
                        {
                            "text": {
                                "content": message
                            }
                        }
                    ]
                }
            }
        )
        print(f"✅ Successfully stored message in Notion database!")
        print(f"Page ID: {response['id']}")
        return True
    except Exception as e:
        print(f"❌ Error storing in Notion database: {e}")
        return False

def main():
    """Main function"""
    print("🤖 Welcome to Notion for DS!")
    print("=" * 40)
    
    # Load environment variables
    notion_token, database_id, message_property, name_property = load_environment()
    
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    # Ask user if they want to write
    user_input = input("Do you want to write? (yes/no): ").strip().lower()
    
    if user_input == "yes":
        print("📝 Storing test message in Notion database...")
        message = "this is a test message"
        store_in_notion_database(notion, database_id, message, message_property, name_property)
    else:
        print("👋 Goodbye! No message stored in database.")

if __name__ == "__main__":
    main() 