# Instagram Posts Email Notifier

A Python script that monitors Instagram accounts for new posts and automatically sends them to your email with images and captions.

## Features

- Monitors multiple Instagram accounts
- Downloads images from new posts (excludes reels and videos)
- Sends email notifications with:
  - Post images as attachments
  - Post caption
  - Post URL
  - Timestamp
- Tracks which posts have been sent to avoid duplicates
- Comprehensive logging
- Configurable via JSON file

## Requirements

- Python 3.7+
- `instaloader` library

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create your configuration file:
```bash
cp config.example.json config.json
```

4. Edit `config.json` with your settings (see Configuration section below)

## Configuration

Edit `config.json` with your settings:

```json
{
  "instagram_accounts": [
    "username1",
    "username2"
  ],
  "instagram_username": "your_instagram_username",
  "instagram_password": "your_instagram_password",
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your_email@gmail.com",
  "sender_password": "your_app_password",
  "recipient_email": "recipient@example.com",
  "max_posts_check": 10,
  "tracking_file": "tracked_posts.json",
  "download_dir": "downloads",
  "log_file": "instagram_notifier.log",
  "log_level": "INFO"
}
```

### Configuration Options

- **instagram_accounts**: List of Instagram usernames to monitor (without @ symbol)
- **instagram_username**: Your Instagram username (optional, but recommended to avoid rate limits)
- **instagram_password**: Your Instagram password (optional, but recommended)
- **smtp_server**: SMTP server for sending emails (e.g., smtp.gmail.com for Gmail)
- **smtp_port**: SMTP port (usually 587 for TLS)
- **sender_email**: Email address to send from
- **sender_password**: Password or app-specific password for sender email
- **recipient_email**: Email address to receive notifications
- **max_posts_check**: Maximum number of recent posts to check per account (default: 10)
- **tracking_file**: File to store tracked posts (default: tracked_posts.json)
- **download_dir**: Directory to store downloaded images (default: downloads)
- **log_file**: Log file path (default: instagram_notifier.log)
- **log_level**: Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO)

### Gmail Setup

If using Gmail, you'll need to:

1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the generated 16-character password
   - Use this as `sender_password` in config.json

### Instagram Login (Optional but Recommended)

While you can use the script without logging in, logging in with your Instagram account helps:
- Access private profiles you follow
- Avoid rate limiting
- More reliable access to posts

**Note**: Instagram credentials are only used locally and never shared.

## Usage

Run the script:

```bash
python instagram_posts_emailer.py
```

### Running Automatically

You can schedule the script to run automatically using:

**Linux/Mac (cron):**

Edit your crontab:
```bash
crontab -e
```

Add a line to run every hour:
```
0 * * * * cd /path/to/script && python instagram_posts_emailer.py
```

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily at specific time)
4. Set action to run: `python C:\path\to\instagram_posts_emailer.py`

## How It Works

1. **Loads Configuration**: Reads settings from `config.json`
2. **Loads Tracking Data**: Reads `tracked_posts.json` to know which posts have been sent
3. **Fetches Posts**: For each monitored account, fetches recent posts
4. **Filters New Posts**: Identifies posts that haven't been sent yet (excludes reels and videos)
5. **Downloads Images**: Downloads images from new posts
6. **Sends Email**: Sends an email with images and caption for each new post
7. **Updates Tracking**: Records sent posts in `tracked_posts.json`

## File Structure

```
.
├── instagram_posts_emailer.py   # Main script
├── config.json                  # Your configuration (create from example)
├── config.example.json          # Example configuration
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── tracked_posts.json           # Auto-generated tracking file
├── instagram_notifier.log       # Auto-generated log file
└── downloads/                   # Auto-generated downloads directory
    └── username/
        └── post_shortcode/
            └── images...
```

## Troubleshooting

### "instaloader not installed" Error
Run: `pip install -r requirements.txt`

### Email Not Sending
- Verify SMTP settings in config.json
- For Gmail, ensure you're using an App Password, not your regular password
- Check firewall/antivirus isn't blocking SMTP connections

### Instagram Login Failed
- Verify username and password in config.json
- Instagram may require verification if logging in from a new location
- You can still run without login, but some features may be limited

### No New Posts Found
- The script only processes posts it hasn't seen before
- Delete `tracked_posts.json` to reset tracking (will re-send all recent posts)
- Check that the Instagram usernames are correct (without @ symbol)

### Script Finds Reels/Videos
The script is designed to skip reels and videos and only process image posts. If you want to include videos, you can modify the script.

## Privacy and Security

- Your Instagram credentials are stored locally and only used to authenticate with Instagram
- Email credentials are stored locally and only used to send emails
- Downloaded images are stored locally in the `downloads` directory
- Consider using environment variables for sensitive credentials in production

## Limitations

- Only processes image posts (not reels, videos, or stories)
- Requires Instagram credentials for reliable access
- Subject to Instagram's rate limits
- SMTP email sending may have daily limits depending on provider

## License

This script is provided as-is for personal use. Use responsibly and in accordance with Instagram's Terms of Service.
