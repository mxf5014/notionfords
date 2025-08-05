#!/usr/bin/env python3
"""
Notion for DS - A simple program to write messages to Notion pages
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
            page_id = secret_data.get('page_id')
            
            if not notion_token or not page_id:
                print("Error: NOTION_API secret must contain 'token' and 'page_id'")
                print(f"Available keys: {list(secret_data.keys())}")
                sys.exit(1)
                
            print("✅ Successfully parsed NOTION_API secret")
            return notion_token, page_id
        except json.JSONDecodeError as e:
            print(f"Error: NOTION_API secret must be valid JSON: {e}")
            print(f"Secret preview: {notion_api_secret[:100]}...")
            sys.exit(1)
    
    # Fallback to individual environment variables
    notion_token = os.getenv('NOTION_TOKEN')
    page_id = os.getenv('NOTION_PAGE_ID')
    
    if not notion_token:
        print("Error: NOTION_TOKEN not found in environment variables")
        print("Please create a .env file with your Notion integration token")
        print("Or set up NOTION_API GitHub secret with token and page_id")
        sys.exit(1)
        
    if not page_id:
        print("Error: NOTION_PAGE_ID not found in environment variables")
        print("Please create a .env file with your Notion page ID")
        print("Or set up NOTION_API GitHub secret with token and page_id")
        sys.exit(1)
        
    return notion_token, page_id

def write_to_notion(client, page_id, message):
    """Write a message to the specified Notion page"""
    try:
        # Create a new block with the message
        response = client.blocks.children.append(
            page_id,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": message
                                }
                            }
                        ]
                    }
                }
            ]
        )
        print(f"✅ Successfully wrote message to Notion page!")
        return True
    except Exception as e:
        print(f"❌ Error writing to Notion: {e}")
        return False

def main():
    """Main function"""
    print("🤖 Welcome to Notion for DS!")
    print("=" * 40)
    
    # Load environment variables
    notion_token, page_id = load_environment()
    
    # Initialize Notion client
    notion = Client(auth=notion_token)
    
    # Ask user if they want to write
    user_input = input("Do you want to write? (yes/no): ").strip().lower()
    
    if user_input == "yes":
        print("📝 Writing test message to Notion page...")
        message = "this is a test message"
        write_to_notion(notion, page_id, message)
    else:
        print("👋 Goodbye! No message written to Notion.")

if __name__ == "__main__":
    main() 