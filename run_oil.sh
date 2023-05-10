#!/bin/bash
export root=$HOME/Documents/scripts
cd $root
python3 oil.py
cd output
git checkout
echo "Script ran at $(date)" >> $root/logs/oil_"$(date '+%Y-%m-%d')".log
echo "Script has run $(wc -l < $root/logs/oil_"$(date '+%Y-%m-%d')".log) times" >> $root/logs/oil_"$(date '+%Y-%m-%d')".log