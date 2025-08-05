#!/usr/bin/env python3
"""
Debug script to check environment variables and .env file
"""

import os
import json

def debug_environment():
    """Debug environment variables and .env file"""
    print("🔍 Debugging Environment Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file_exists = os.path.exists('.env')
    print(f"✅ .env file exists: {env_file_exists}")
    
    if env_file_exists:
        print("\n📄 .env file contents:")
        try:
            with open('.env', 'r') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    
    # Try to load dotenv
    print("\n🔄 Loading dotenv...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ dotenv loaded successfully")
    except ImportError:
        print("❌ python-dotenv not installed")
        return
    except Exception as e:
        print(f"❌ Error loading dotenv: {e}")
        return
    
    # Check environment variables
    print("\n🔍 Checking environment variables:")
    
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    notion_api = os.getenv('NOTION_API')
    
    print(f"NOTION_TOKEN found: {'Yes' if notion_token else 'No'}")
    if notion_token:
        print(f"NOTION_TOKEN length: {len(notion_token)}")
        print(f"NOTION_TOKEN preview: {notion_token[:10]}...")
    
    print(f"NOTION_DATABASE_ID found: {'Yes' if database_id else 'No'}")
    if database_id:
        print(f"NOTION_DATABASE_ID: {database_id}")
        print(f"NOTION_DATABASE_ID length: {len(database_id)}")
    
    print(f"NOTION_API found: {'Yes' if notion_api else 'No'}")
    if notion_api:
        print(f"NOTION_API length: {len(notion_api)}")
        try:
            secret_data = json.loads(notion_api)
            print("✅ NOTION_API is valid JSON")
            print(f"Keys: {list(secret_data.keys())}")
        except json.JSONDecodeError as e:
            print(f"❌ NOTION_API is not valid JSON: {e}")
    
    # Check if we can create a Notion client
    print("\n🤖 Testing Notion client creation:")
    try:
        from notion_client import Client
        
        if notion_token:
            client = Client(auth=notion_token)
            print("✅ Notion client created successfully")
            
            # Test a simple API call
            try:
                response = client.users.me()
                print("✅ Notion API connection successful")
                print(f"User: {response.get('name', 'Unknown')}")
            except Exception as e:
                print(f"❌ Notion API connection failed: {e}")
        else:
            print("❌ Cannot create Notion client - no token available")
            
    except ImportError:
        print("❌ notion-client not installed")
    except Exception as e:
        print(f"❌ Error creating Notion client: {e}")
    
    # Summary
    print("\n📊 Summary:")
    if notion_token and database_id:
        print("✅ Local environment configured correctly")
    elif notion_api:
        print("✅ GitHub secret configured")
    else:
        print("❌ No Notion credentials found")
        print("\nTo fix this:")
        print("1. Make sure your .env file has NOTION_TOKEN and NOTION_DATABASE_ID")
        print("2. Or set up NOTION_API GitHub secret")
        print("3. Run: python setup-local.py")

if __name__ == "__main__":
    debug_environment() 