# Usage Guide

## First Run

On first run, you'll need to authenticate with Telegram:

1. Run the application:
   ```bash
   python -m src.main
   ```
2. Enter your phone number when prompted (international format: +1234567890)
3. Enter the verification code sent to your Telegram
4. The session will be saved for future use

## Analyzing Groups

1. The tool will display a list of all your groups
2. Enter the number corresponding to the group you want to analyze
3. The tool will calculate the total size of all media without downloading

## Understanding Results

The analysis shows:
- Total estimated storage requirements
- Media breakdown by type:
  - Photos
  - Videos
  - Documents
  - Audio files
- File counts for each media type

## Troubleshooting

If you encounter any issues:
1. Ensure your `.env` file is properly configured
2. Check your internet connection
3. Verify your Telegram API credentials
4. Delete the `.session` file and try again if authentication fails
