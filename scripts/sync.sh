#!/bin/bash

echo "🔄 Syncing Git repository..."

# Stage all changes
git add .

# Commit with timestamp
git commit -m "Manual sync: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to origin main
git push origin main

echo "✅ Sync complete."
