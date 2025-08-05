#!/usr/bin/env python3
"""
Flask web app for Notion for DS
"""

import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from notion_client import Client

app = Flask(__name__)

def load_environment():
    """Load environment variables from .env file or GitHub secrets"""
    load_dotenv()
    
    # Check for GitHub secret first (for deployment)
    notion_api_secret = os.getenv('NOTION_API')
    
    if notion_api_secret:
        try:
            # Parse the JSON secret
            secret_data = json.loads(notion_api_secret)
            notion_token = secret_data.get('token')
            database_id = secret_data.get('database_id')
            
            if not notion_token or not database_id:
                return None, None
                
            return notion_token, database_id
        except json.JSONDecodeError:
            return None, None
    
    # Fallback to individual environment variables (for local development)
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    
    return notion_token, database_id

def store_in_notion_database(client, database_id, message):
    """Store a message in the specified Notion database"""
    try:
        # First try to create with Message as title property
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
        return True, response['id']
    except Exception as e:
        error_message = str(e)
        if "expected to be a relation" in error_message:
            try:
                # Create a new page with just a title (no Message property)
                response = client.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        "Name": {
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
                return True, response['id']
            except Exception as e2:
                return False, f"Error creating new entry: {e2}"
        else:
            return False, str(e)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def store_message():
    """Store a message in Notion database"""
    try:
        # Get message from request
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'success': False, 'error': 'No message provided'})
        
        # Load environment
        notion_token, database_id = load_environment()
        
        if not notion_token or not database_id:
            return jsonify({'success': False, 'error': 'Notion credentials not configured'})
        
        # Initialize Notion client
        notion = Client(auth=notion_token)
        
        # Store message
        success, result = store_in_notion_database(notion, database_id, message)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Message stored successfully',
                'page_id': result
            })
        else:
            return jsonify({'success': False, 'error': result})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    """Health check endpoint"""
    notion_token, database_id = load_environment()
    return jsonify({
        'status': 'healthy',
        'notion_configured': bool(notion_token and database_id)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 