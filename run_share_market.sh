#!/bin/bash
export root=$HOME/Documents/scripts

# Set the path to your share_market.py script
SHARE_MARKET_SCRIPT=$root"/share_market.py"

OUTPUT_FOLDER=$root"/output"

# Define the start and end times (in 24-hour format)
START_TIME="11:00"
END_TIME="15:00"


folder=$root/logs/$(date +%Y-%m-%d)  # Get today's date in the format YYYY-MM-DD

if [ ! -d "$folder" ]; then
    mkdir "$folder"
fi

log_file="$folder/share_market.log"

count=0

if [ -f "$log_file" ]; then
    count=$(wc -l < "$log_file")
fi


# Calculate the duration between the start and end times (in seconds)
START_SECONDS=$(date -d "$START_TIME" +%s)
END_SECONDS=$(date -d "$END_TIME" +%s)
DURATION=$((END_SECONDS - START_SECONDS))

# Run the script at 2-minute intervals within the specified time range
while true; do
    CURRENT_TIME=$(date +"%T")
    CURRENT_SECONDS=$(date -d "$CURRENT_TIME" +%s)

    if ((CURRENT_SECONDS >= START_SECONDS && CURRENT_SECONDS <= END_SECONDS)); then
        python3 $SHARE_MARKET_SCRIPT
        ((count++))

        # git checkout to the output folder
        git -C "$OUTPUT_FOLDER" checkout

        echo "Script ran at $(date)" >> "$log_file"
        echo "Script has run $count times" >> "$log_file"

    fi

    if ((CURRENT_SECONDS >= END_SECONDS)); then
        break
    fi

    sleep 120  # Sleep for 2 minutes before the next iteration
done