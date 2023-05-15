#!/bin/bash
export root=$HOME/Documents/scripts
cd $root
python3 gold.py
cd output
git checkout
echo "Script ran at $(date)" >> $root/logs/"$(date '+%Y-%m-%d')"/gold.log
echo "Script has run $(wc -l < $root/logs/"$(date '+%Y-%m-%d')"/gold.log) times" >> $root/logs/"$(date '+%Y-%m-%d')"/gold.log