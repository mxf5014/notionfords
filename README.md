# Notion for DS

A simple Python program that allows you to write messages to Notion pages through the Notion API.

## Features

- Interactive command-line interface
- Writes messages to specified Notion pages
- Environment-based configuration
- Error handling and user feedback

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the integration token

### 3. Get Your Notion Page ID

1. Open the Notion page where you want to write messages
2. Copy the page ID from the URL:
   - URL format: `https://www.notion.so/Your-Page-Title-1234567890abcdef1234567890abcdef`
   - Page ID: `1234567890abcdef1234567890abcdef`

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

### 5. Share Your Page with the Integration

1. Open your Notion page
2. Click "Share" in the top right
3. Click "Invite" and search for your integration name
4. Add the integration to the page

## Usage

### Local Development

Run the program:

```bash
python main.py
```

The program will:
1. Ask "Do you want to write?"
2. If you answer "yes", it will write "this is a test message" to your Notion page
3. Provide feedback on success or failure

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
📝 Writing test message to Notion page...
✅ Successfully wrote message to Notion page!
```

## Requirements

- Python 3.7+
- Notion API access
- Valid Notion integration token
- Page ID with proper permissions

 test
