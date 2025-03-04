# Unanet Timesheet Automation

This script automatically fills in 8 hours for the ODOS project in Unanet timesheet every day at 10 AM.

## Prerequisites

1. Python 3.9 or higher
2. Chrome browser
3. Virtual environment (`.venv` folder in the project directory)

OR

- Docker

## Setup Instructions

### Option 1: Local Setup

#### 1. Start Chrome in Debug Mode

Run Chrome with remote debugging enabled:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

#### 2. Log into Unanet

1. Open Chrome (the debug instance)
2. Navigate to https://amivero.unanet.biz/amivero/action/time
3. Log in with your credentials
4. Keep Chrome running

#### 3. Run the Script Manually

To test the script:
```bash
python auto_timesheet_entry.py
```

The script will:
1. Connect to Chrome
2. Navigate to the timesheet
3. Find the ODOS project row
4. Enter 8 hours for today
5. Save the timesheet

#### 4. Automated Daily Runs

The script is configured to run automatically at 10 AM every day using launchd.

##### Launch Agent Status
- Check if running: `launchctl list | grep chacezanaty`
- View logs: 
  ```bash
  cat timesheet.log  # For standard output
  cat timesheet.error.log  # For errors
  ```

##### Launch Agent Management
- Stop automation: 
  ```bash
  launchctl unload ~/Library/LaunchAgents/com.chacezanaty.timesheet.plist
  ```
- Start automation: 
  ```bash
  launchctl load ~/Library/LaunchAgents/com.chacezanaty.timesheet.plist
  ```

### Option 2: Docker Setup

#### 1. Build the Docker Image

```bash
docker build -t timesheet-automation .
```

#### 2. Run the Container

```bash
docker run -d \
  --name timesheet \
  -v $(pwd)/logs:/app/logs \
  timesheet-automation
```

#### 3. View Logs

```bash
docker logs -f timesheet
```

#### 4. Stop the Container

```bash
docker stop timesheet
```

## Customizing for Different Timesheets

To modify this script for a different timesheet:

1. Fork this repository
2. Modify the following in `auto_timesheet_entry.py`:
   - URL in `driver.get()`
   - Project name in the search condition
   - Hours value if different from 8
3. Update the launch agent or Docker schedule as needed

## File Structure

- `auto_timesheet_entry.py` - Main script
- `com.chacezanaty.timesheet.plist` - Launch agent configuration
- `Dockerfile` - Docker configuration
- `requirements.txt` - Python dependencies
- `timesheet.log` - Script output log
- `timesheet.error.log` - Error log

## Important Notes

1. Chrome must be running in debug mode for local setup
2. You must be logged into Unanet
3. The script will automatically enter 8 hours for the ODOS project
4. Logs are saved in the project directory
5. Docker setup handles Chrome installation automatically

## Troubleshooting

1. If the script fails to connect to Chrome:
   - For local setup: Make sure Chrome is running with `--remote-debugging-port=9222`
   - For Docker: Check container logs for Chrome startup issues

2. If the script can't find the ODOS row:
   - Make sure you're logged into Unanet
   - Check the error logs

3. If the launch agent isn't running (local setup):
   - Check the launch agent status
   - Try unloading and loading it again
   - Check the log files for errors

4. Docker container issues:
   - Check logs: `docker logs timesheet`
   - Restart container: `docker restart timesheet`
   - Rebuild image: `docker build --no-cache -t timesheet-automation .` 