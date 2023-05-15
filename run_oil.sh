#!/bin/bash
export root=$HOME/Documents/scripts

folder=$root/logs/$(date +%Y-%m-%d)  # Get today's date in the format YYYY-MM-DD

if [ ! -d "$folder" ]; then
    mkdir "$folder"
fi

log_file="$folder/oil.log"

count=0

if [ -f "$log_file" ]; then
    count=$(wc -l < "$log_file")
fi


cd $root
python3 oil.py
((count++))
cd output
git checkout
echo "Script ran at $(date)" >> "$log_file"
echo "Script has run $count times" >> "$log_file"
