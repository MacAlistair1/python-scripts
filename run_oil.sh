#!/bin/bash
cd /home/superx/Documents/scripts
python3 oil.py
cd output
git checkout
echo "Script ran at $(date)" >> /home/superx/Documents/scripts/run.log
echo "Script has run $(wc -l < /home/superx/Documents/scripts/run.log) times" >> /home/superx/Documents/scripts/run.log
