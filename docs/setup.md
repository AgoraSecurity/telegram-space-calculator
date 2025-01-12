# Setup Guide

## Getting Telegram API Credentials

1. Visit https://my.telegram.org
2. Log in with your phone number
3. Go to 'API development tools'
4. Create a new application
5. Copy the `api_id` and `api_hash`

## Environment Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   ```
