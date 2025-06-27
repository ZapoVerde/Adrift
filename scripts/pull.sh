#!/bin/bash

echo "🔽 Pulling latest changes from GitHub..."

# Pull using rebase to avoid extra merge commits
git pull --rebase origin main

if [ $? -eq 0 ]; then
    echo "✅ Pull complete."
else
    echo "❌ Pull failed — resolve conflicts manually."
fi
