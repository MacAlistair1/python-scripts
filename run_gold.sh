#!/bin/bash
export root=$HOME/Documents/scripts
cd $root
python3 gold.py
cd output
git checkout
echo "Script ran at $(date)" >> $root/logs/gold_"$(date '+%Y-%m-%d')".log
echo "Script has run $(wc -l < $root/logs/gold_"$(date '+%Y-%m-%d')".log) times" >> $root/logs/gold_"$(date '+%Y-%m-%d')".log