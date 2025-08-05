# Notion for DS

A Python application that integrates with Notion databases to store and manage data through both a web interface and command-line interface.

## Features

- **Web Interface**: Modern Flask-based web application with admin panel
- **Command Line Interface**: Simple CLI for quick data entry
- **Master Code System**: Advanced routing system for barcode-like inputs
- **Environment-based Configuration**: Secure credential management
- **Configurable Database Properties**: Flexible property naming for any database schema
- **Error Handling**: Comprehensive error handling and user feedback
- **Multiple Deployment Options**: Support for local, Heroku, and GitHub Actions

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/notionfords.git
cd notionfords
```

### 2. Install Dependencies

#### Option A: Using pip (Standard Python)

```bash
pip install -r requirements.txt
```

#### Option B: Using Conda (Recommended)

```bash
conda env create -f environment.yml
conda activate notionfords
```

### 3. Set up Notion Integration

1. **Create Notion Integration**:
   - Go to [Notion Integrations](https://www.notion.so/my-integrations)
   - Create a new integration
   - Copy the integration token

2. **Create Notion Database**:
   - Create a new database in Notion
   - Add a "Title" property for your messages (default: "Message" or "Name")
   - Copy the database ID from the URL:
     - URL format: `https://www.notion.so/Your-Workspace/1234567890abcdef1234567890abcdef?v=...`
     - Database ID: `1234567890abcdef1234567890abcdef`

3. **Share Database with Integration**:
   - Open your Notion database
   - Click "Share" in the top right
   - Click "Invite" and search for your integration name
   - Add the integration to the database

### 4. Configure Environment Variables

#### Local Development

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   NOTION_TOKEN=your_actual_notion_token
   NOTION_DATABASE_ID=your_actual_database_id
   NOTION_GUIDE_DATABASE_ID=your_guide_database_id_optional
   
   # Database Property Names (Configurable)
   # Main Database Properties
   NOTION_MESSAGE_PROPERTY=Message
   NOTION_NAME_PROPERTY=Name
   NOTION_BARCODE_PROPERTIES=barcode,Barcode,BARCODE
   
   # Guide Database Properties
   NOTION_MASTERCODE_PROPERTY=Mastercode
   NOTION_ROUTE_PROPERTY=Route
   ```

#### GitHub Actions (Optional)

1. Go to your GitHub repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Create a new repository secret named `NOTION_API`
4. Set the value as JSON:
   ```json
   {
     "token": "your_actual_notion_token",
     "database_id": "your_actual_database_id"
   }
   ```

## Usage

### Web Application

Start the web application:

```bash
python app.py
```

The application will:
- Start on `http://localhost:5001`
- Open your browser automatically
- Provide a web interface for data entry
- Include an admin panel at `/admin` for configuration

### Command Line Interface

Run the simple CLI version:

```bash
python main.py
```

The CLI will:
- Ask "Do you want to write?"
- If you answer "yes", it will store "this is a test message" in your Notion database
- Provide feedback on success or failure

### Master Code System

The application supports an advanced master code system:

1. **Guide Database**: Create a separate Notion database with columns:
   - `Mastercode` (Title): The master code (e.g., "1234")
   - `Route` (Text): The route value to apply

2. **Configuration**: Add your guide database ID to the `.env` file:
   ```
   NOTION_GUIDE_DATABASE_ID=your_guide_database_id
   ```

3. **Usage**: When a master code is entered, it will:
   - Look up the route in the guide database
   - Apply the route to the previous entry's barcode field
   - Or create a new entry with the route as the message

## Database Configuration

### Configurable Properties

The application supports configurable database property names to work with any Notion database schema:

#### Main Database Properties
- **`NOTION_MESSAGE_PROPERTY`**: Primary message property (default: "Message")
- **`NOTION_NAME_PROPERTY`**: Fallback message property (default: "Name")
- **`NOTION_BARCODE_PROPERTIES`**: Comma-separated list of barcode properties (default: "barcode,Barcode,BARCODE")

#### Guide Database Properties
- **`NOTION_MASTERCODE_PROPERTY`**: Master code lookup property (default: "Mastercode")
- **`NOTION_ROUTE_PROPERTY`**: Route value property (default: "Route")

### Example Database Schemas

#### Simple Message Database
```
Properties:
- Message (Title) - Your messages
```

#### Advanced Database with Barcode
```
Properties:
- Message (Title) - Your messages
- Barcode (Select) - Route assignments
```

#### Guide Database for Master Codes
```
Properties:
- Mastercode (Title) - Master codes (e.g., "1234")
- Route (Text) - Route values (e.g., "Route A")
```

## Deployment

### Local Development

```bash
python app.py
```

### Heroku Deployment

The project includes a `Procfile` for Heroku deployment:

```bash
heroku create your-app-name
git push heroku main
```

### GitHub Actions

The repository includes GitHub Actions workflows for automated testing:

- **notion-test.yml**: Tests Notion integration
- **python-app.yml**: General Python application testing

## Project Structure

```
notionfords/
├── app.py                 # Main Flask web application
├── main.py               # Simple CLI version
├── templates/            # Web UI templates
│   ├── index.html       # Main interface
│   └── admin.html       # Admin panel
├── requirements.txt      # Python dependencies
├── environment.yml      # Conda environment
├── env.example          # Environment template
├── Procfile            # Heroku deployment
├── runtime.txt         # Python runtime
├── .github/workflows/  # CI/CD workflows
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Endpoints

### Web Application

- `GET /` - Main interface
- `GET /admin` - Admin panel
- `POST /store` - Store message in Notion
- `POST /admin/update` - Update credentials
- `POST /admin/test` - Test credentials
- `GET /health` - Health check

### Environment Variables

- `NOTION_TOKEN` - Your Notion integration token
- `NOTION_DATABASE_ID` - Your Notion database ID
- `NOTION_GUIDE_DATABASE_ID` - Optional guide database ID for master codes
- `NOTION_MESSAGE_PROPERTY` - Main message property name
- `NOTION_NAME_PROPERTY` - Fallback message property name
- `NOTION_BARCODE_PROPERTIES` - Comma-separated barcode property names
- `NOTION_MASTERCODE_PROPERTY` - Master code property name
- `NOTION_ROUTE_PROPERTY` - Route property name

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Create an issue on GitHub
- Check the existing issues for solutions
- Review the documentation above

---

**Note**: This application requires valid Notion API credentials and proper database permissions to function correctly. The configurable properties allow you to work with any Notion database schema.
