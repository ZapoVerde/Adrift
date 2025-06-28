#!/bin/bash

# 📄 git_pull_rebase.sh
# This script finds your git root, changes to it, and runs a safe pull with rebase.

# ✅ How to run this script:
# 1. Save this file in your Replit workspace (e.g., as git_pull_rebase.sh)
# 2. Make it executable:
#    chmod +x git_pull_rebase.sh
# 3. Run it any time with:
#    ./git_pull_rebase.sh

# 🔍 Step 1: Find the top-level git directory
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ $? -ne 0 ]; then
  echo "❌ Not inside a Git repository. Navigate to your project folder first."
  exit 1
fi

# 🚀 Step 2: Change to the root and pull
cd "$GIT_ROOT"
echo "📂 Changed to Git root: $GIT_ROOT"

echo "🔄 Pulling latest changes with rebase..."
git pull --rebase origin main
