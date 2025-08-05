#!/usr/bin/env python3
"""
Simple test script to verify GitHub secret setup
"""

import os
import json

def test_secret():
    print("🧪 Testing GitHub Secret Setup")
    print("=" * 40)
    
    # Check if NOTION_API is available
    notion_api = os.getenv('NOTION_API')
    
    if not notion_api:
        print("❌ NOTION_API secret not found!")
        print("\nTo fix this:")
        print("1. Go to your GitHub repository")
        print("2. Click Settings → Secrets and variables → Actions")
        print("3. Create a new repository secret named 'NOTION_API'")
        print("4. Set the value to JSON format:")
        print("   {")
        print('     "token": "secret_your_token_here",')
        print('     "page_id": "your_page_id_here"')
        print("   }")
        return False
    
    print("✅ NOTION_API secret found!")
    
    try:
        # Parse the JSON
        data = json.loads(notion_api)
        
        # Check required fields
        if 'token' not in data:
            print("❌ Missing 'token' in NOTION_API secret")
            return False
            
        if 'page_id' not in data:
            print("❌ Missing 'page_id' in NOTION_API secret")
            return False
        
        print("✅ Secret contains required fields")
        print(f"Token length: {len(data['token'])}")
        print(f"Page ID: {data['page_id']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in NOTION_API secret: {e}")
        print("Make sure your secret is valid JSON format")
        return False

if __name__ == "__main__":
    success = test_secret()
    if success:
        print("\n🎉 Secret setup looks good!")
    else:
        print("\n🔧 Please fix the issues above and try again") 