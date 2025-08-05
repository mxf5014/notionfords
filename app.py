#!/usr/bin/env python3
"""
Flask web app for Notion for DS
"""

import os
import json
import sys
import webbrowser
import threading
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from notion_client import Client

# Handle PyInstaller bundled environment
if getattr(sys, 'frozen', False):
    # Running in a bundle
    template_dir = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_dir)
else:
    # Running in normal Python environment
    app = Flask(__name__)

# Global variable to track the last entry ID
last_entry_id = None

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    # Load individual environment variables
    notion_token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv('NOTION_DATABASE_ID')
    guide_database_id = os.getenv('NOTION_GUIDE_DATABASE_ID')
    
    # Load configurable database properties
    message_property = os.getenv('NOTION_MESSAGE_PROPERTY', 'Message')
    name_property = os.getenv('NOTION_NAME_PROPERTY', 'Name')
    barcode_properties = os.getenv('NOTION_BARCODE_PROPERTIES', 'barcode,Barcode,BARCODE').split(',')
    mastercode_property = os.getenv('NOTION_MASTERCODE_PROPERTY', 'Mastercode')
    route_property = os.getenv('NOTION_ROUTE_PROPERTY', 'Route')
    
    return notion_token, database_id, guide_database_id, message_property, name_property, barcode_properties, mastercode_property, route_property

def update_env_file(token, database_id, guide_database_id="", message_property="Message", name_property="Name", barcode_properties="barcode,Barcode,BARCODE", mastercode_property="Mastercode", route_property="Route"):
    """Update the .env file with new credentials"""
    try:
        env_content = f"""# Notion API Configuration
NOTION_TOKEN={token}
NOTION_DATABASE_ID={database_id}
NOTION_GUIDE_DATABASE_ID={guide_database_id}

# Database Property Names (Configurable)
# Main Database Properties
NOTION_MESSAGE_PROPERTY={message_property}
NOTION_NAME_PROPERTY={name_property}
NOTION_BARCODE_PROPERTIES={barcode_properties}

# Guide Database Properties
NOTION_MASTERCODE_PROPERTY={mastercode_property}
NOTION_ROUTE_PROPERTY={route_property}
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        return True, "Environment variables updated successfully"
    except Exception as e:
        return False, f"Error updating .env file: {str(e)}"

def get_current_env():
    """Get current environment variables for display"""
    load_dotenv()
    return {
        'NOTION_TOKEN': os.getenv('NOTION_TOKEN', ''),
        'NOTION_DATABASE_ID': os.getenv('NOTION_DATABASE_ID', ''),
        'NOTION_GUIDE_DATABASE_ID': os.getenv('NOTION_GUIDE_DATABASE_ID', ''),
        'NOTION_MESSAGE_PROPERTY': os.getenv('NOTION_MESSAGE_PROPERTY', 'Message'),
        'NOTION_NAME_PROPERTY': os.getenv('NOTION_NAME_PROPERTY', 'Name'),
        'NOTION_BARCODE_PROPERTIES': os.getenv('NOTION_BARCODE_PROPERTIES', 'barcode,Barcode,BARCODE'),
        'NOTION_MASTERCODE_PROPERTY': os.getenv('NOTION_MASTERCODE_PROPERTY', 'Mastercode'),
        'NOTION_ROUTE_PROPERTY': os.getenv('NOTION_ROUTE_PROPERTY', 'Route')
    }

def check_guide_database(client, guide_database_id, mastercode, mastercode_property='Mastercode', route_property='Route'):
    """Check if a mastercode exists in the Guide database and return the route"""
    try:
        # Query the Guide database for the mastercode
        response = client.databases.query(
            database_id=guide_database_id,
            filter={
                "property": mastercode_property,
                "title": {
                    "equals": mastercode
                }
            }
        )
        
        if response['results']:
            # Found a match, get the route
            page = response['results'][0]
            route_property_data = page['properties'].get(route_property, {})
            
            if route_property_data.get('type') == 'rich_text' and route_property_data['rich_text']:
                return True, route_property_data['rich_text'][0]['text']['content']
            elif route_property_data.get('type') == 'title' and route_property_data['title']:
                return True, route_property_data['title'][0]['text']['content']
            else:
                return True, "Route not found"
        else:
            return False, None
            
    except Exception as e:
        return False, f"Error checking Guide database: {str(e)}"

def update_previous_entry(client, database_id, page_id, barcode_value, barcode_properties=['barcode', 'Barcode', 'BARCODE']):
    """Update the barcode field of a previous entry"""
    try:
        # First, let's get the current page to see the exact property structure
        current_page = client.pages.retrieve(page_id)
        properties = current_page.get('properties', {})
        
        print(f"🔍 Current page properties: {list(properties.keys())}")
        
        # Try different property name variations
        barcode_prop_name = None
        for prop_name in barcode_properties:
            if prop_name in properties:
                barcode_prop_name = prop_name
                break
        
        if not barcode_prop_name:
            return False, "Barcode property not found"
        
        print(f"🔍 Using barcode property: {barcode_prop_name}")
        
        # Update the barcode field
        client.pages.update(
            page_id=page_id,
            properties={
                barcode_prop_name: {
                    "select": {
                        "name": barcode_value
                    }
                }
            }
        )
        return True, "Barcode updated successfully"
    except Exception as e:
        return False, f"Error updating barcode: {str(e)}"

def get_last_entry_id(client, database_id):
    """Get the ID of the most recent entry in the database"""
    try:
        response = client.databases.query(
            database_id=database_id,
            sorts=[{
                "property": "created time",
                "direction": "descending"
            }],
            page_size=1
        )
        
        if response['results']:
            return response['results'][0]['id']
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error getting last entry: {e}")
        return None

def store_in_notion_database(client, database_id, message, guide_database_id=None, message_property='Message', name_property='Name'):
    """Store a message in the specified Notion database"""
    try:
        # First try to create with Message as title property
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
        return True, response['id']
    except Exception as e:
        error_message = str(e)
        if "expected to be a relation" in error_message:
            try:
                # Create a new page with just a title (no Message property)
                response = client.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        name_property: {
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
    try:
        return render_template('index.html')
    except Exception as e:
        # Fallback for bundling issues
        return f"""
        <html>
        <head><title>Notion for DS</title></head>
        <body>
            <h1>Notion for DS</h1>
            <p>Template loading error: {str(e)}</p>
            <p>Please ensure templates are properly bundled.</p>
        </body>
        </html>
        """

@app.route('/admin')
def admin():
    """Admin panel"""
    try:
        current_env = get_current_env()
        return render_template('admin.html', env=current_env)
    except Exception as e:
        return f"""
        <html>
        <head><title>Admin - Notion for DS</title></head>
        <body>
            <h1>Admin Panel</h1>
            <p>Template loading error: {str(e)}</p>
        </body>
        </html>
        """

@app.route('/admin/update', methods=['POST'])
def update_credentials():
    """Update environment variables"""
    try:
        data = request.get_json()
        token = data.get('token', '').strip()
        database_id = data.get('database_id', '').strip()
        guide_database_id = data.get('guide_database_id', '').strip()
        message_property = data.get('message_property', 'Message').strip()
        name_property = data.get('name_property', 'Name').strip()
        barcode_properties = data.get('barcode_properties', 'barcode,Barcode,BARCODE').strip()
        mastercode_property = data.get('mastercode_property', 'Mastercode').strip()
        route_property = data.get('route_property', 'Route').strip()
        
        if not token or not database_id:
            return jsonify({'success': False, 'error': 'Both token and database ID are required'})
        
        # Update .env file
        success, message = update_env_file(token, database_id, guide_database_id, message_property, name_property, barcode_properties, mastercode_property, route_property)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/test', methods=['POST'])
def test_credentials():
    """Test the provided credentials"""
    try:
        data = request.get_json()
        token = data.get('token', '').strip()
        database_id = data.get('database_id', '').strip()
        
        if not token or not database_id:
            return jsonify({'success': False, 'error': 'Both token and database ID are required'})
        
        # Test the credentials
        try:
            notion = Client(auth=token)
            # Try to get database info
            database = notion.databases.retrieve(database_id)
            return jsonify({
                'success': True, 
                'message': 'Credentials are valid!',
                'database_name': database.get('title', [{}])[0].get('text', {}).get('content', 'Unknown')
            })
        except Exception as e:
            return jsonify({'success': False, 'error': f'Invalid credentials: {str(e)}'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/store', methods=['POST'])
def store_message():
    """Store a message in Notion database"""
    global last_entry_id
    
    try:
        # Get message from request
        data = request.get_json()
        message = data.get('message', '')
        
        print(f"🔍 Received message: {message}")
        
        if not message:
            return jsonify({'success': False, 'error': 'No message provided'})
        
        # Load environment
        notion_token, database_id, guide_database_id, message_property, name_property, barcode_properties, mastercode_property, route_property = load_environment()
        
        print(f"🔍 Environment loaded:")
        print(f"  - Database ID: {database_id}")
        print(f"  - Guide Database ID: {guide_database_id}")
        
        if not notion_token or not database_id:
            return jsonify({'success': False, 'error': 'Notion credentials not configured'})
        
        # Initialize Notion client
        notion = Client(auth=notion_token)
        
        # Check if this is a master code in the Guide database
        if guide_database_id:
            print(f"🔍 Checking Guide database for master code: {message}")
            is_mastercode, route_value = check_guide_database(notion, guide_database_id, message, mastercode_property, route_property)
            
            print(f"🔍 Master code check result:")
            print(f"  - Is master code: {is_mastercode}")
            print(f"  - Route value: {route_value}")
            
            if is_mastercode:
                print(f"🔍 Processing as master code")
                # This is a master code, update the previous entry's barcode
                
                # Try to use the global last entry ID first, then fall back to database query
                entry_to_update = last_entry_id if last_entry_id else get_last_entry_id(notion, database_id)
                
                print(f"🔍 Entry to update: {entry_to_update}")
                
                if entry_to_update:
                    success, result = update_previous_entry(notion, database_id, entry_to_update, route_value, barcode_properties)
                    print(f"🔍 Update result: {success}, {result}")
                    
                    if success:
                        return jsonify({
                            'success': True,
                            'message': f'Master code processed. Route "{route_value}" added to previous entry.',
                            'page_id': entry_to_update,
                            'is_mastercode': True
                        })
                    else:
                        return jsonify({'success': False, 'error': result})
                else:
                    # No previous entry found, create a new entry with the route as the message
                    print(f"🔍 No previous entry found, creating new entry with route")
                    success, result = store_in_notion_database(notion, database_id, route_value, guide_database_id, message_property, name_property)
                    
                    if success:
                        # Update global last entry ID
                        last_entry_id = result
                        
                        return jsonify({
                            'success': True,
                            'message': f'Master code processed. Created new entry with route "{route_value}".',
                            'page_id': result,
                            'is_mastercode': True
                        })
                    else:
                        return jsonify({'success': False, 'error': result})
            else:
                print(f"🔍 Not a master code, processing as normal message")
        else:
            print(f"🔍 No Guide database configured, processing as normal message")
        
        # Not a master code, store as normal message
        success, result = store_in_notion_database(notion, database_id, message, guide_database_id, message_property, name_property)
        
        print(f"🔍 Store result: {success}, {result}")
        
        if success:
            # Update global last entry ID
            last_entry_id = result
            
            return jsonify({
                'success': True, 
                'message': 'Message stored successfully',
                'page_id': result,
                'is_mastercode': False
            })
        else:
            return jsonify({'success': False, 'error': result})
            
    except Exception as e:
        print(f"❌ Error in store_message: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    """Health check endpoint"""
    notion_token, database_id, guide_database_id = load_environment()
    return jsonify({
        'status': 'healthy',
        'notion_configured': bool(notion_token and database_id),
        'guide_configured': bool(notion_token and guide_database_id)
    })

def open_browser(port):
    """Open browser after a short delay to ensure Flask is running"""
    time.sleep(1.5)  # Wait for Flask to start
    webbrowser.open(f'http://localhost:{port}')

if __name__ == '__main__':
    # Production-safe settings for PyInstaller bundling
    port = int(os.environ.get('PORT', 5001))  # Changed default port to avoid conflicts
    
    # Open browser automatically (only when run directly, not in production)
    if not getattr(sys, 'frozen', False):  # Only open browser in development
        browser_thread = threading.Thread(target=open_browser, args=(port,))
        browser_thread.daemon = True
        browser_thread.start()
    
    app.run(
        debug=False,  # Disable debug mode for production
        use_reloader=False,  # Disable reloader for bundled apps
        host='0.0.0.0', 
        port=port
    ) 