#!/bin/bash

# 📄 git_push_main.sh
# This script finds your Git root, changes to it, stages everything, commits (with a prompt), and pushes to origin/main.

# ✅ How to run this script:
# 1. Save this file in your Replit workspace (e.g., as git_push_main.sh)
# 2. Make it executable:
#    chmod +x git_push_main.sh
# 3. Run it any time with:
#    ./git_push_main.sh

# 🔍 Step 1: Find the top-level Git directory
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ $? -ne 0 ]; then
  echo "❌ Not inside a Git repository. Navigate to your project folder first."
  exit 1
fi

cd "$GIT_ROOT"
echo "📂 Changed to Git root: $GIT_ROOT"

# 🗃️ Step 2: Stage all changes
git add .

# 📝 Step 3: Ask user for commit message
echo "📝 Enter commit message:"
read COMMIT_MSG

# 💾 Step 4: Commit changes
git commit -m "$COMMIT_MSG"

# 🚀 Step 5: Push to origin/main
echo "🔼 Pushing to origin/main..."
git push origin main

