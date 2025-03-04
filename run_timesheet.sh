#!/bin/bash

# Change to the script directory
cd /Users/chacezanaty/Documents/auto_schedule_time_sheet

# Create logs directory if it doesn't exist
mkdir -p logs

# Get current timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")

# Activate virtual environment
source .venv/bin/activate

# Run the timesheet script and capture output
{
    python3 auto_timesheet_entry.py 2>&1
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "$(date): Timesheet automation completed successfully" >> logs/timesheet.log
    else
        echo "$(date): Timesheet automation failed with exit code $exit_code" >> logs/timesheet.log
    fi
} | tee "logs/timesheet_${timestamp}.log" 