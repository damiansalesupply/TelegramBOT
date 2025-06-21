# Telegram Bot with OpenAI Assistant Integration

## Overview

This is a Python-based Telegram bot that integrates with OpenAI's Assistant API to provide intelligent conversational responses. The bot receives messages from Telegram users and forwards them to an OpenAI Assistant, then returns the AI-generated responses back to the users.

## System Architecture

### Core Architecture
- **Event-Driven Design**: The bot uses Telegram's webhook/polling mechanism to receive messages and responds asynchronously
- **Service-Oriented Pattern**: Clear separation between bot handling, OpenAI service, and configuration management
- **Modular Structure**: Each component has a single responsibility (configuration, bot handling, OpenAI integration, utilities)

### Technology Stack
- **Python 3.11**: Main programming language
- **python-telegram-bot**: Official Telegram Bot API wrapper
- **OpenAI Python SDK**: For Assistant API integration
- **python-dotenv**: Environment variable management
- **UV**: Modern Python package manager

## Key Components

### 1. Configuration Management (`config.py`)
- Centralizes all environment variable handling
- Validates required configuration on startup
- Manages API keys, tokens, and operational settings
- Provides secure credential handling with masked display
- NEW: Handles whitelist configuration and logging preferences

### 2. Bot Handler (`bot_handler.py`)
- Processes incoming Telegram messages
- Coordinates between Telegram API and OpenAI service
- Handles user interactions and error responses
- Implements typing indicators for better UX
- NEW: User authorization checking against whitelist
- NEW: Integration with logging and thread management services

### 3. OpenAI Service (`openai_service.py`)
- Manages OpenAI Assistant API communication
- Creates conversation threads for each user interaction
- Handles API retries and error scenarios
- Processes assistant responses asynchronously
- NEW: Supports persistent thread context for continuous conversations

### 4. Thread Manager (`thread_manager.py`)
- NEW: Manages conversation threads per user for context persistence
- Stores thread mappings in local JSON file
- Provides thread creation, retrieval, and cleanup functions
- Maintains conversation continuity across sessions

### 5. Logging Service (`logging_service.py`)
- NEW: Comprehensive conversation logging system
- CSV file logging with automatic header creation
- Google Sheets integration for real-time logging
- Configurable logging options (can disable CSV or Sheets independently)

### 6. Command Handler (`command_handler.py`)
- NEW: Handles administrative bot commands
- /reset - Clear user's conversation context
- /stats - Display bot statistics and configuration status
- Authorization checks for all commands

### 7. Main Application (`main.py`)
- Entry point for the application
- Sets up logging and configuration
- Initializes bot handlers and message filters
- Manages the bot's lifecycle
- NEW: Integrates all new services and command handlers

### 8. Utilities (`utils.py`)
- Logging configuration and setup
- Text processing helper functions
- Common utility functions for the application

## Data Flow

1. **Message Reception**: User sends message to Telegram bot
2. **Authorization Check**: Bot verifies user is in whitelist (if enabled)
3. **Thread Management**: Bot retrieves or creates persistent conversation thread for user
4. **Message Processing**: Bot handler receives update from Telegram
5. **AI Processing**: Message forwarded to OpenAI Assistant via API with thread context
6. **Response Generation**: Assistant generates intelligent response using conversation history
7. **Response Delivery**: Bot sends response back to user via Telegram
8. **Logging**: Conversation is logged to CSV file and Google Sheets (if enabled)

## External Dependencies

### Required Services
- **Telegram Bot API**: For bot functionality and message handling
- **OpenAI Assistant API**: For AI-powered conversation responses

### Required Configuration
- `TELEGRAM_TOKEN`: Bot token from @BotFather
- `OPENAI_API_KEY`: API key from OpenAI platform
- `ASSISTANT_ID`: Pre-configured OpenAI Assistant ID

### Optional Configuration
- `LOG_LEVEL`: Logging verbosity (default: INFO)
- `MAX_RETRIES`: API retry attempts (default: 3)
- `TIMEOUT_SECONDS`: Request timeout (default: 60)
- `ALLOWED_USERS`: Comma-separated Telegram user IDs for whitelist access control
- `SHEET_NAME`: Google Sheets document name for logging (default: SupportLogs)
- `ENABLE_CSV_LOGGING`: Enable/disable CSV conversation logging (default: true)
- `ENABLE_SHEETS_LOGGING`: Enable/disable Google Sheets logging (default: true)
- `CREDENTIALS_FILE`: Path to Google service account credentials (default: credentials.json)

## Deployment Strategy

### Development Environment
- Uses Replit with Python 3.11 module
- UV package manager for dependency management
- Environment variables configured via .env file

### Production Considerations
- Stateless design enables horizontal scaling
- Environment-based configuration for different deployments
- Comprehensive logging for monitoring and debugging
- Error handling with user-friendly messages

### Deployment Configuration
- Automated dependency installation via UV
- Enhanced startup script with deployment fixes: `python start.py`
- Cloud Run autoscale deployment support with proper port binding
- Webhook support for production environments
- Single instance management to prevent conflicts
- Health check endpoints for deployment monitoring
- Parallel workflow support in Replit environment

## Changelog

- June 21, 2025. Initial setup
- June 21, 2025. Added advanced features:
  - User whitelist authorization system
  - Persistent conversation threads per user
  - CSV and Google Sheets logging integration
  - Administrative commands (/reset, /stats)
  - Thread management and context persistence
  - Comprehensive logging service with configurable options
- June 21, 2025. Applied deployment fixes for Cloud Run autoscale:
  - Added webhook support for production deployments
  - Implemented proper port binding (0.0.0.0:PORT)
  - Created health check endpoints (/health, /)
  - Added single instance management to prevent conflicts
  - Enhanced environment detection and configuration
  - Added deployment scripts and documentation
- June 21, 2025. PRODUCTION DEPLOYMENT SUCCESS:
  - Resolved all webhook conflicts and polling issues
  - Implemented polling-only mode with conflict detection
  - Verified bot functionality with OpenAI Assistant (asst_qgWQNNJGV0bGPy35Rdif4qpb)
  - Confirmed message processing, authorization, and logging systems
  - Polish error messages implemented (❌ Błąd: format)
  - Bot fully operational and ready for Cloud Run deployment
- June 21, 2025. FINAL DEPLOYMENT CONFIGURATION:
  - Auto-configured webhook URL for Replit deployments
  - Implemented proper environment detection (dev/prod modes)
  - Added health check endpoints for deployment stability
  - Deploy script with conflict prevention and mode switching
  - Ready for Autoscale deployment with build command: ./deploy_script.sh

## User Preferences

Preferred communication style: Simple, everyday language.
Request: Add new advanced features including whitelist, context memory, and logging capabilities.