# Timesheet Automation

This script automatically fills in your timesheet in Unanet every day at a specified time.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/MonsoudZ/timesheet-automation.git
cd timesheet-automation
```

### 2. Set Up Configuration

1. Copy the template configuration file:
```bash
cp config.template.py config.py
```

2. Edit `config.py` with your settings:
```python
# Your company's Unanet URL
UNANET_URL = "https://your-company.unanet.biz/action/time"

# Your project code exactly as it appears in Unanet
PROJECT_CODE = "YOUR.PROJECT.CODE"

# Number of hours to enter (as a string)
HOURS_TO_ENTER = "8"
```

**Important**: `config.py` contains sensitive information and is excluded from git. Never commit this file!

### 3. Choose Your Setup Method

#### Option A: Local Setup (macOS)

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start Chrome in Debug Mode:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

4. Log into Unanet:
   - In the debug Chrome instance, go to your company's Unanet URL
   - Log in with your credentials
   - Keep Chrome running

5. Set up automated runs:
   - Copy the launch agent to your LaunchAgents directory:
   ```bash
   cp com.chacezanaty.timesheet.plist ~/Library/LaunchAgents/
   ```
   - Edit the plist file to update paths to match your setup:
   ```bash
   nano ~/Library/LaunchAgents/com.chacezanaty.timesheet.plist
   ```
   - Load the launch agent:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.chacezanaty.timesheet.plist
   ```

#### Option B: Docker Setup

1. Build the Docker image:
```bash
docker build -t timesheet-automation .
```

2. Create a logs directory:
```bash
mkdir logs
```

3. Run the container:
```bash
docker run -d \
  --name timesheet \
  -v $(pwd)/logs:/app/logs \
  timesheet-automation
```

### 4. Customize for Your Needs

1. Edit `auto_timesheet_entry.py`:
   - Update the URL to your company's Unanet instance:
   ```python
   driver.get("https://YOUR-COMPANY.unanet.biz/action/time")
   ```
   - Change the project name search to your project code:
   ```python
   if value == "YOUR.PROJECT.CODE":
   ```
   - Modify default hours if needed:
   ```python
   input_field.send_keys("YOUR_HOURS")  # Default is "8"
   ```

2. Update the schedule:
   - For local setup, edit the plist file's StartCalendarInterval
   - For Docker, add `-e CRON_SCHEDULE="0 10 * * *"` to your docker run command

## Testing Your Setup

1. Run the script manually first:
```bash
python auto_timesheet_entry.py
```

2. Check the logs:
```bash
cat timesheet.log  # For output
cat timesheet.error.log  # For errors
```

## Troubleshooting

1. Chrome Connection Issues:
   - Ensure Chrome is running in debug mode (port 9222)
   - Check if you can access your Unanet instance in the debug Chrome instance
   - Verify your network connection

2. Authentication Issues:
   - Make sure you're logged into Unanet in the debug Chrome instance
   - Check if your session is still valid

3. Project Not Found:
   - Verify your project code matches exactly what's in your Unanet system
   - Check the timesheet.log for the actual project values being found

4. Docker Issues:
   - Check container logs: `docker logs timesheet`
   - Ensure Chrome is working in the container: `docker exec timesheet google-chrome --version`

## Security Notes

1. Never commit sensitive information:
   - Credentials
   - API keys
   - Personal information
   - Configuration files with sensitive data
   - Company-specific URLs or project codes

2. The script assumes you're already logged into Unanet
   - Keep your debug Chrome instance secure
   - Lock your computer when away
   - Do not share your debug Chrome profile

## Support

If you encounter issues:
1. Check the logs
2. Review the Troubleshooting section
3. Open an issue on GitHub with:
   - Error messages
   - Steps to reproduce
   - Your setup details (OS, Python version, etc.)
   - DO NOT include any sensitive company information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Remove any sensitive information
5. Submit a pull request

## License

This project is open source and available under the MIT License. 