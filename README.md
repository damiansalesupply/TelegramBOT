# Telegram Bot with OpenAI Assistant Integration

A professional Telegram bot that integrates with OpenAI's Assistant API to provide intelligent conversational responses with advanced features like user whitelisting, conversation logging, and persistent context.

## Features

### Core Functionality
- **OpenAI Assistant Integration**: Uses OpenAI's Assistant API for intelligent responses
- **Telegram Bot**: Full Telegram Bot API integration with async message handling
- **Persistent Context**: Maintains conversation context per user using threads
- **Error Handling**: Comprehensive error handling with user-friendly messages

### Security & Access Control
- **User Whitelist**: Restrict bot access to specific Telegram users
- **Authorization Checks**: All commands and messages require proper authorization

### Logging & Analytics
- **CSV Logging**: Automatic logging of all conversations to CSV file
- **Google Sheets Integration**: Real-time logging to Google Sheets
- **Conversation Tracking**: Complete audit trail of user interactions

### Management Commands
- `/reset` - Clear conversation context and start fresh
- `/stats` - View bot statistics and configuration status

## Quick Start

1. **Install Dependencies**
   ```bash
   uv add python-telegram-bot gspread oauth2client
   ```

2. **Configure Environment Variables**
   Copy `.env.example` to `.env` and fill in your credentials:
   ```
   TELEGRAM_TOKEN=your_bot_token_from_botfather
   OPENAI_API_KEY=your_openai_api_key
   ASSISTANT_ID=your_assistant_id
   ```

3. **Run the Bot**
   ```bash
   python main.py
   ```

## Configuration Options

### Required Variables
- `TELEGRAM_TOKEN`: Get from @BotFather on Telegram
- `OPENAI_API_KEY`: Get from OpenAI Platform
- `ASSISTANT_ID`: Create an assistant on OpenAI Platform

### Optional Variables
- `ALLOWED_USERS`: Comma-separated Telegram user IDs (leave empty to allow all)
- `SHEET_NAME`: Google Sheets document name (default: "SupportLogs")
- `ENABLE_CSV_LOGGING`: Enable/disable CSV logging (default: true)
- `ENABLE_SHEETS_LOGGING`: Enable/disable Google Sheets logging (default: true)
- `LOG_LEVEL`: Logging verbosity (default: INFO)

## Google Sheets Setup

1. **Create Service Account**
   - Go to Google Cloud Console
   - Create a new project or select existing
   - Enable Google Sheets API
   - Create service account credentials
   - Download JSON credentials file

2. **Configure Credentials**
   - Rename downloaded file to `credentials.json`
   - Place in project root directory
   - Share your Google Sheet with the service account email

3. **Create Spreadsheet**
   - Create a Google Sheet named "SupportLogs" (or your configured name)
   - The bot will automatically add headers on first run

## Getting User IDs for Whitelist

To find Telegram user IDs for the whitelist:

1. **Method 1: Use @userinfobot**
   - Message @userinfobot on Telegram
   - It will reply with your user ID

2. **Method 2: Check bot logs**
   - Temporarily disable whitelist (empty ALLOWED_USERS)
   - Send a message to your bot
   - Check logs for user ID
   - Add ID to whitelist and restart bot

## File Structure

```
├── main.py              # Application entry point
├── config.py            # Configuration management
├── bot_handler.py       # Message handling logic
├── openai_service.py    # OpenAI API integration
├── logging_service.py   # CSV and Sheets logging
├── thread_manager.py    # Conversation context management
├── command_handler.py   # Bot commands (/reset, /stats)
├── utils.py            # Utility functions
├── .env.example        # Environment variables template
└── credentials.json.example  # Google credentials template
```

## Usage Examples

### Basic Conversation
```
User: Hello, can you help me?
Bot: Hello! I'm here to help. What can I assist you with today?
```

### Reset Context
```
User: /reset
Bot: ✅ Conversation context has been reset. Starting fresh!
```

### View Statistics
```
User: /stats
Bot: 📊 Bot Statistics:
• Active conversations: 5
• Total threads: 12
• CSV logging: ✅
• Sheets logging: ✅
• Whitelist: ✅
```

## Logging Format

Both CSV and Google Sheets logging use the same format:
- Timestamp
- User ID
- User Name
- Question
- Answer

## Troubleshooting

### Common Issues

1. **"Missing required environment variables"**
   - Check your .env file contains all required variables
   - Verify variable names match exactly

2. **"You don't have access to this bot"**
   - Your Telegram user ID is not in the ALLOWED_USERS list
   - Check user ID using @userinfobot
   - Add your ID to the whitelist

3. **Google Sheets logging fails**
   - Verify credentials.json file exists and is valid
   - Check if the sheet is shared with service account email
   - Ensure Google Sheets API is enabled in Google Cloud Console

4. **Bot doesn't respond**
   - Check bot token is correct
   - Verify assistant ID exists and is accessible
   - Check OpenAI API key permissions

### Debug Mode

Enable debug logging by setting:
```
LOG_LEVEL=DEBUG
```

This will show detailed information about:
- Message processing
- OpenAI API calls
- Thread management
- Logging operations

## Security Considerations

- Keep your `.env` file secure and never commit it to version control
- Use environment variables for all sensitive data
- Regularly rotate API keys
- Monitor bot usage through logs
- Implement proper user whitelisting in production

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review bot logs for error messages
3. Verify all configuration variables are set correctly
4. Test with a simple message to isolate the problem