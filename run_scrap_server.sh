#!/bin/bash
export root=$HOME/scripts/scrap

folder=$root/logs/$(date +%Y-%m-%d)  # Get today's date in the format YYYY-MM-DD

if [ ! -d "$folder" ]; then
    mkdir "$folder"
fi

log_file="$folder/scrap.log"

cd $root
source ~/virtualenv/scripts/3.12/bin/activate
echo "Scrap started at $(date)" >> "$log_file"
python bank_rate.py; python currency.py; python gold-silver.py;  python oil.py; python earthquake.py;  python share_market.py; python top_music_video.py; python top_singer.py; python patro.py; python channel_info.py; python latest_youtube_video.py; python latest_reel.py;  python earthquake.py; python rashifal.py;
cd output
git checkout
printf "Scrap ended at $(date) \n\n" >> "$log_file"
