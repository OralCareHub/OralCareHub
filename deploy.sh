#!/bin/bash
# ==============================================================
# OralCareHub - Deploy website to GitHub Pages
# Run: bash deploy.sh
# ==============================================================

set -e

REPO_NAME="oralcarehub"
SITE_DIR="site"

echo "=============================="
echo "  OralCareHub Deploy Script"
echo "=============================="

# Check gh is authenticated
if ! gh auth status &>/dev/null; then
    echo ""
    echo "ERROR: GitHub CLI not logged in."
    echo "Run: gh auth login"
    echo "Select: GitHub.com > HTTPS > Login with browser"
    exit 1
fi

GITHUB_USER=$(gh api user --jq '.login')
echo "Logged in as: $GITHUB_USER"

# Check if repo exists
if gh repo view "$GITHUB_USER/$REPO_NAME" &>/dev/null; then
    echo "Repo $REPO_NAME already exists. Updating..."
else
    echo "Creating repo $GITHUB_USER/$REPO_NAME..."
    gh repo create "$REPO_NAME" --public --description "OralCareHub - Dental health tips and product reviews" --clone=false
    echo "Repo created!"
fi

# Set up git remote
cd "$(dirname "$0")"

if git remote get-url origin &>/dev/null; then
    git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
else
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
fi

# Push to GitHub
git add -A
git diff --cached --quiet || git commit -m "Update OralCareHub site and content"
git branch -M main
git push -u origin main

# Enable GitHub Pages on the site/ directory
echo "Enabling GitHub Pages..."
gh api repos/$GITHUB_USER/$REPO_NAME/pages \
    --method POST \
    --field "source[branch]=main" \
    --field "source[path]=/site" 2>/dev/null || \
gh api repos/$GITHUB_USER/$REPO_NAME/pages \
    --method PUT \
    --field "source[branch]=main" \
    --field "source[path]=/site" 2>/dev/null || true

echo ""
echo "=============================="
echo "  DEPLOYED!"
echo ""
echo "  Your site will be live at:"
echo "  https://$GITHUB_USER.github.io/$REPO_NAME/"
echo ""
echo "  (May take 1-2 minutes to go live)"
echo "=============================="
