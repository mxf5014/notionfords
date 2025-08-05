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
    """Load environment variables from .env file or GitHub secrets"""
    load_dotenv()
    
    # Check for GitHub secret first
    notion_api_secret = os.getenv('NOTION_API')
    
    print(f"🔍 Checking for NOTION_API secret...")
    print(f"NOTION_API found: {'Yes' if notion_api_secret else 'No'}")
    
    if notion_api_secret:
        print(f"NOTION_API length: {len(notion_api_secret)}")
        try:
            # Parse the JSON secret
            secret_data = json.loads(notion_api_secret)
            notion_token = secret_data.get('token')
            database_id = secret_data.get('database_id')
            
            if not notion_token or not database_id:
                print("Error: NOTION_API secret must contain 'token' and 'database_id'")
                print(f"Available keys: {list(secret_data.keys())}")
                sys.exit(1)
                
            print("✅ Successfully parsed NOTION_API secret")
            return notion_token, database_id
        except json.JSONDecodeError as e:
            print(f"Error: NOTION_API secret must be valid JSON: {e}")
            print(f"Secret preview: {notion_api_secret[:100]}...")
            sys.exit(1)
    
    # Fallback to individual environment variables
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    if not notion_token:
        print("Error: NOTION_TOKEN not found in environment variables")
        print("Please create a .env file with your Notion integration token")
        print("Or set up NOTION_API GitHub secret with token and database_id")
        sys.exit(1)
        
    if not database_id:
        print("Error: NOTION_DATABASE_ID not found in environment variables")
        print("Please create a .env file with your Notion database ID")
        print("Or set up NOTION_API GitHub secret with token and database_id")
        sys.exit(1)
        
    return notion_token, database_id

def store_in_notion_database(client, database_id, message):
    """Store a message in the specified Notion database"""
    try:
        # Create a new page in the database
        response = client.pages.create(
            parent={"database_id": database_id},
            properties={
                "Message": {
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
    notion_token, database_id = load_environment()
    
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    # Ask user if they want to write
    user_input = input("Do you want to write? (yes/no): ").strip().lower()
    
    if user_input == "yes":
        print("📝 Storing test message in Notion database...")
        message = "this is a test message"
        store_in_notion_database(notion, database_id, message)
    else:
        print("👋 Goodbye! No message stored in database.")

if __name__ == "__main__":
    main() 