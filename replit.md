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

### 2. Bot Handler (`bot_handler.py`)
- Processes incoming Telegram messages
- Coordinates between Telegram API and OpenAI service
- Handles user interactions and error responses
- Implements typing indicators for better UX

### 3. OpenAI Service (`openai_service.py`)
- Manages OpenAI Assistant API communication
- Creates conversation threads for each user interaction
- Handles API retries and error scenarios
- Processes assistant responses asynchronously

### 4. Main Application (`main.py`)
- Entry point for the application
- Sets up logging and configuration
- Initializes bot handlers and message filters
- Manages the bot's lifecycle

### 5. Utilities (`utils.py`)
- Logging configuration and setup
- Text processing helper functions
- Common utility functions for the application

## Data Flow

1. **Message Reception**: User sends message to Telegram bot
2. **Message Processing**: Bot handler receives update from Telegram
3. **AI Processing**: Message forwarded to OpenAI Assistant via API
4. **Thread Management**: OpenAI creates conversation thread and processes message
5. **Response Generation**: Assistant generates intelligent response
6. **Response Delivery**: Bot sends response back to user via Telegram

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
- Single command deployment: `uv add python-telegram-bot && python main.py`
- Parallel workflow support in Replit environment

## Changelog

- June 21, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.