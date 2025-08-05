# Notion for DS

A simple Python program that allows you to store messages in Notion databases through the Notion API.

## Features

- Interactive command-line interface
- Writes messages to specified Notion pages
- Environment-based configuration
- Error handling and user feedback

## Setup

### Option A: Standard Python (pip)

```bash
pip install -r requirements.txt
```

### Option B: Anaconda (Recommended)

1. **Quick Setup**:
   ```bash
   python setup-conda.py
   ```
   This will create the conda environment and set up your credentials.

2. **Manual Setup**:
   ```bash
   conda env create -f environment.yml
   conda activate notionfords
   python setup-local.py
   ```

### 2. Set up Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the integration token

### 3. Create a Notion Database

1. Create a new database in Notion
2. Add a "Title" property called "Message" (this is where your strings will be stored)
3. Copy the database ID from the URL:
   - URL format: `https://www.notion.so/Your-Workspace/1234567890abcdef1234567890abcdef?v=...`
   - Database ID: `1234567890abcdef1234567890abcdef`

### 4. Configure Environment Variables

#### Option A: Local Development (.env file)

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   NOTION_TOKEN=your_actual_notion_token
   NOTION_PAGE_ID=your_actual_page_id
   ```

#### Option B: GitHub Secrets (Recommended for CI/CD)

1. Go to your GitHub repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Create a new repository secret named `NOTION_API`
4. Set the value as JSON:
   ```json
   {
     "token": "your_actual_notion_token",
     "page_id": "your_actual_page_id"
   }
   ```

### 5. Share Your Database with the Integration

1. Open your Notion database
2. Click "Share" in the top right
3. Click "Invite" and search for your integration name
4. Add the integration to the database

## Usage

### Local Development

For local development, you need to set up a `.env` file:

1. **Quick Setup** (recommended):
   ```bash
   python setup-local.py
   ```
   This will prompt you for your credentials and create the `.env` file automatically.

2. **Manual Setup**:
   ```bash
   cp env.example .env
   # Edit .env with your actual credentials
   ```

3. **Run the program**:
   ```bash
   python main.py
   ```

The program will:
1. Ask "Do you want to write?"
2. If you answer "yes", it will store "this is a test message" in your Notion database
3. Provide feedback on success or failure

**Note**: GitHub secrets only work in GitHub Actions workflows, not in your local terminal.

### GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/notion-test.yml`) that:

1. Automatically runs on pushes to main branch
2. Can be manually triggered via "Actions" tab
3. Uses the `NOTION_API` secret for authentication
4. Automatically answers "yes" to the write prompt

To trigger the workflow manually:
1. Go to the "Actions" tab in your GitHub repository
2. Select "Test Notion Integration"
3. Click "Run workflow"

## Example Output

```
🤖 Welcome to Notion for DS!
========================================
Do you want to write? (yes/no): yes
📝 Storing test message in Notion database...
✅ Successfully stored message in Notion database!
Page ID: 1234567890abcdef1234567890abcdef
```

## Requirements

- Python 3.7+
- Notion API access
- Valid Notion integration token
- Page ID with proper permissions

 test
