#!/usr/bin/env python3
"""
Setup script for local development
"""

import os
import json

def setup_local_env():
    print("🔧 Setting up Local Development Environment")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return
    
    print("📝 Creating .env file for local development...")
    
    # Get user input
    print("\nPlease provide your Notion credentials:")
    token = input("Notion Integration Token: ").strip()
    database_id = input("Notion Database ID (32 characters): ").strip()
    
    if not token or not database_id:
        print("❌ Both token and database ID are required!")
        return
    
    # Create .env file
    env_content = f"""# Notion API Configuration
NOTION_TOKEN={token}
NOTION_DATABASE_ID={database_id}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("\nYou can now run: python main.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def check_local_setup():
    print("🔍 Checking Local Setup")
    print("=" * 30)
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Load and check environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        token = os.getenv('NOTION_TOKEN')
        database_id = os.getenv('NOTION_DATABASE_ID')
        
        if token and database_id:
            print("✅ Environment variables loaded")
            print(f"Token length: {len(token)}")
            print(f"Database ID: {database_id}")
            return True
        else:
            print("❌ Missing environment variables in .env file")
            return False
    else:
        print("❌ .env file not found")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_local_setup()
    else:
        setup_local_env() 