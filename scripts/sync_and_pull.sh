#!/bin/bash

echo "🔽 Pulling latest changes from GitHub..."
git pull --rebase origin main

if [ $? -ne 0 ]; then
    echo "❌ Pull failed — sync aborted. Resolve conflicts manually."
    exit 1
fi

echo "🟡 Staging and committing local changes..."
git add .

# Skip commit if there's nothing to commit
if git diff --cached --quiet; then
    echo "⚠️  No local changes to commit."
else
    git commit -m "Manual sync after pull: $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo "🔼 Pushing changes to GitHub..."
git push origin main

echo "✅ Sync and pull complete."
