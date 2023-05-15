#!/bin/bash
export root=$HOME/Documents/scripts
cd $root
python3 oil.py
cd output
git checkout
echo "Script ran at $(date)" >> $root/logs/"$(date '+%Y-%m-%d')"/oil.log
echo "Script has run $(wc -l < $root/logs/"$(date '+%Y-%m-%d')"/oil.log) times" >> $root/logs/"$(date '+%Y-%m-%d')"/oil.log