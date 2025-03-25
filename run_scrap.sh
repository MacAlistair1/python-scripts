#!/bin/bash
export root=$HOME/Documents/scripts

folder=$root/logs/$(date +%Y-%m-%d)  # Get today's date in the format YYYY-MM-DD

if [ ! -d "$folder" ]; then
    mkdir "$folder"
fi

log_file="$folder/scrap.log"

printf "Scrap ran at $(date) \n\n" >> "$log_file"