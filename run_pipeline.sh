#!/bin/bash

# 1. Check for Drift
python src/monitor.py
STATUS=$?

# 2. If exit code is 100, trigger retraining
if [ $STATUS -eq 100 ]; then
    print "🔄 Starting Automated Retraining..."
    python src/train.py
    python src/promote_model.py
    print "🚀 System Healed: New model is now @champion."
else
    print "😴 Everything is fine. No action needed."
fi