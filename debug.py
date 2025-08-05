#!/usr/bin/env python3
"""
Debug script to check environment variables and GitHub secrets
"""

import os
import json

def debug_environment():
    """Debug environment variables and secrets"""
    print("🔍 Debugging Environment Variables")
    print("=" * 50)
    
    # Check for NOTION_API secret
    notion_api = os.getenv('NOTION_API')
    print(f"NOTION_API found: {'Yes' if notion_api else 'No'}")
    
    if notion_api:
        print(f"NOTION_API length: {len(notion_api)}")
        print(f"NOTION_API preview: {notion_api[:50]}...")
        
        try:
            secret_data = json.loads(notion_api)
            print("✅ NOTION_API is valid JSON")
            print(f"Keys found: {list(secret_data.keys())}")
            
            if 'token' in secret_data:
                print(f"Token length: {len(secret_data['token'])}")
            else:
                print("❌ 'token' key not found")
                
            if 'page_id' in secret_data:
                print(f"Page ID: {secret_data['page_id']}")
            else:
                print("❌ 'page_id' key not found")
                
        except json.JSONDecodeError as e:
            print(f"❌ NOTION_API is not valid JSON: {e}")
    
    # Check for individual environment variables
    notion_token = os.getenv('NOTION_TOKEN')
    page_id = os.getenv('NOTION_PAGE_ID')
    
    print(f"\nIndividual variables:")
    print(f"NOTION_TOKEN found: {'Yes' if notion_token else 'No'}")
    print(f"NOTION_PAGE_ID found: {'Yes' if page_id else 'No'}")
    
    # List all environment variables (excluding sensitive ones)
    print(f"\nAll environment variables:")
    for key, value in os.environ.items():
        if 'NOTION' in key or 'GITHUB' in key:
            if 'TOKEN' in key or 'SECRET' in key:
                print(f"{key}: {'*' * len(value)} (hidden)")
            else:
                print(f"{key}: {value}")

if __name__ == "__main__":
    debug_environment() 