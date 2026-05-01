#!/bin/bash
# ==============================================================
# OralCareHub - Publish articles to all platforms
#
# Usage:
#   bash publish.sh                    # Publish ALL articles
#   bash publish.sh --dry-run          # Preview without posting
#   bash publish.sh article-name.md    # Publish specific article
# ==============================================================

set -e

cd "$(dirname "$0")/automation"

if [ "$1" == "--dry-run" ]; then
    echo "DRY RUN MODE - nothing will be posted"
    python3 publisher.py --dry-run ../content/articles/*.md
elif [ -n "$1" ]; then
    python3 publisher.py "../content/articles/$1"
else
    python3 publisher.py ../content/articles/*.md
fi
