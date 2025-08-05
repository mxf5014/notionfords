#!/usr/bin/env python3
"""
Setup script for Anaconda users
"""

import os
import subprocess
import sys

def check_conda_environment():
    """Check if we're in the right conda environment"""
    print("🔍 Checking Conda Environment")
    print("=" * 40)
    
    # Check if conda is available
    try:
        result = subprocess.run(['conda', 'info', '--envs'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Conda not found or not working properly")
            return False
    except FileNotFoundError:
        print("❌ Conda not found. Please install Anaconda first.")
        return False
    
    # Check current environment
    current_env = os.environ.get('CONDA_DEFAULT_ENV', 'base')
    print(f"Current conda environment: {current_env}")
    
    if current_env == 'notionfords':
        print("✅ You're in the correct environment!")
        return True
    else:
        print("⚠️  You're not in the 'notionfords' environment")
        print("Run: conda activate notionfords")
        return False

def setup_conda_environment():
    """Set up the conda environment"""
    print("🔧 Setting up Conda Environment")
    print("=" * 40)
    
    # Check if environment already exists
    result = subprocess.run(['conda', 'env', 'list'], 
                          capture_output=True, text=True)
    
    if 'notionfords' in result.stdout:
        print("✅ Environment 'notionfords' already exists")
        print("To activate it, run: conda activate notionfords")
        return True
    
    # Create environment
    print("📦 Creating conda environment 'notionfords'...")
    result = subprocess.run(['conda', 'env', 'create', '-f', 'environment.yml'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Environment created successfully!")
        print("To activate it, run: conda activate notionfords")
        return True
    else:
        print("❌ Error creating environment:")
        print(result.stderr)
        return False

def setup_local_env():
    """Set up local environment variables"""
    print("\n🔧 Setting up Local Environment")
    print("=" * 40)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file for local development...")
    
    # Get user input
    print("\nPlease provide your Notion credentials:")
    token = input("Notion Integration Token: ").strip()
    database_id = input("Notion Database ID (32 characters): ").strip()
    
    if not token or not database_id:
        print("❌ Both token and database ID are required!")
        return False
    
    # Create .env file
    env_content = f"""# Notion API Configuration
NOTION_TOKEN={token}
NOTION_DATABASE_ID={database_id}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Anaconda Setup for Notion for DS")
    print("=" * 50)
    
    # Step 1: Set up conda environment
    if not setup_conda_environment():
        return
    
    # Step 2: Set up local environment
    if not setup_local_env():
        return
    
    print("\n🎉 Setup Complete!")
    print("\nNext steps:")
    print("1. Activate the environment: conda activate notionfords")
    print("2. Run the program: python main.py")
    print("3. Or test the setup: python setup-local.py check")

if __name__ == "__main__":
    main() 