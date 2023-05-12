#!/bin/bash
export root=$HOME/Documents/scripts
cd $root
python3 silver.py
cd output
git checkout
echo "Script ran at $(date)" >> $root/logs/silver_"$(date '+%Y-%m-%d')".log
echo "Script has run $(wc -l < $root/logs/silver_"$(date '+%Y-%m-%d')".log) times" >> $root/logs/silver_"$(date '+%Y-%m-%d')".log